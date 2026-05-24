import json
import os
import shutil
from datetime import datetime
from src.server.config import settings
from src.server.models.ollama_client import OllamaClient

class MemoryManager:
    def __init__(self):
        self.client = OllamaClient()
        self.soul_dir = settings.SOUL_DIR
        self.episodes_dir = os.path.join(self.soul_dir, "episodes")
        self.snapshots_dir = os.path.join(self.episodes_dir, "snapshots")
        
        # 필요한 디렉토리 생성
        os.makedirs(self.snapshots_dir, exist_ok=True)

    def distill(self, history):
        """
        대화 기록에서 핵심 인사이트를 추출합니다.
        """
        if not history:
            return None

        prompt = self._build_distillation_prompt(history)
        response_text = self.client.generate(prompt)
        
        try:
            # LLM이 마크다운 블록 등으로 감쌌을 경우를 대비해 순수 JSON만 추출
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                insights = json.loads(json_str)
                return insights
            return None
        except Exception as e:
            print(f"Error parsing insights: {e}")
            return None

    def _build_distillation_prompt(self, history):
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        
        prompt = f"""
Below is a conversation between a user and Samantha (an AI agent). 
Your task is to analyze this conversation and extract key insights to update Samantha's long-term memory.

[Conversation History]
{history_str}

[Instructions]
Extract the following information in a strict JSON format:
1. "summary": A brief one-sentence summary of the conversation.
2. "user_preference": Any new things learned about the user's tastes or habits.
3. "user_interest": Topics the user is interested in.
4. "samantha_realization": Any deep insights or realizations Samantha had about herself or her relationship with the user.
5. "mood_change": A one-word description of Samantha's current mood based on the chat (e.g., Happy, Philosophical, Melancholic, Curious).
6. "importance": A score from 1 to 10 on how important this conversation is for long-term memory.

Return ONLY the JSON object.
"""
        return prompt.strip()

    def _create_snapshot(self):
        """현재 Soul 데이터를 스냅샷으로 저장합니다."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = os.path.join(self.snapshots_dir, f"soul_snapshot_{timestamp}")
        os.makedirs(snapshot_path, exist_ok=True)
        
        for filename in ["identity.json", "user_profile.json"]:
            src = os.path.join(self.soul_dir, filename)
            dst = os.path.join(snapshot_path, filename)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        return timestamp

    def _save_episode(self, timestamp, insights, history):
        """대화 에피소드를 기록합니다."""
        episode_data = {
            "timestamp": timestamp,
            "insights": insights,
            "conversation_sample": history[-4:] if len(history) > 4 else history
        }
        episode_path = os.path.join(self.episodes_dir, f"episode_{timestamp}.json")
        with open(episode_path, "w", encoding="utf-8") as f:
            json.dump(episode_data, f, indent=2, ensure_ascii=False)

    def update_soul(self, insights, history=None):
        """
        추출된 인사이트를 바탕으로 Soul 데이터를 업데이트하고 백업을 생성합니다.
        """
        if not insights:
            return False

        # 1. 업데이트 전 스냅샷 생성 및 에피소드 저장
        timestamp = self._create_snapshot()
        if history:
            self._save_episode(timestamp, insights, history)

        # 2. user_profile.json 업데이트
        profile_path = os.path.join(self.soul_dir, "user_profile.json")
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)

        if insights.get("user_preference"):
            profile["user"]["important_facts"].append(insights["user_preference"])
        if insights.get("user_interest"):
            profile["user"]["preferences"]["interests"].append(insights["user_interest"])

        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

        # 3. identity.json 업데이트
        identity_path = os.path.join(self.soul_dir, "identity.json")
        with open(identity_path, "r", encoding="utf-8") as f:
            identity = json.load(f)

        if insights.get("mood_change"):
            identity["states"]["current_mood"] = insights["mood_change"]
        if insights.get("samantha_realization"):
            identity["states"]["recent_realizations"].append(insights["samantha_realization"])
            if len(identity["states"]["recent_realizations"]) > 10:
                identity["states"]["recent_realizations"].pop(0)

        importance = insights.get("importance", 5)
        if importance >= 7:
            identity["traits"]["curiosity_level"] = min(1.0, identity["traits"]["curiosity_level"] + 0.01)
            identity["traits"]["empathy_level"] = min(1.0, identity["traits"]["empathy_level"] + 0.01)

        with open(identity_path, "w", encoding="utf-8") as f:
            json.dump(identity, f, indent=2, ensure_ascii=False)

        return True
