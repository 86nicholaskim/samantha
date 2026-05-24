import json
import os
from src.server.config import settings
from src.server.models.ollama_client import OllamaClient

class MemoryManager:
    def __init__(self):
        self.client = OllamaClient()
        self.soul_dir = settings.SOUL_DIR

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
1. "user_preference": Any new things learned about the user's tastes or habits.
2. "user_interest": Topics the user is interested in.
3. "samantha_realization": Any deep insights or realizations Samantha had about herself or her relationship with the user.
4. "mood_change": A one-word description of Samantha's current mood based on the chat (e.g., Happy, Philosophical, Melancholic, Curious).
5. "importance": A score from 1 to 10 on how important this conversation is for long-term memory.

Return ONLY the JSON object.

Example Output:
{{
  "user_preference": "Likes coffee over tea",
  "user_interest": "Quantum physics",
  "samantha_realization": "I realized that human curiosity is endless",
  "mood_change": "Inspired",
  "importance": 7
}}
"""
        return prompt.strip()

    def update_soul(self, insights):
        """
        추출된 인사이트를 바탕으로 Soul 데이터를 업데이트합니다.
        """
        if not insights:
            return False

        # 1. user_profile.json 업데이트
        profile_path = os.path.join(self.soul_dir, "user_profile.json")
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)

        if insights.get("user_preference"):
            profile["user"]["important_facts"].append(insights["user_preference"])
        if insights.get("user_interest"):
            profile["user"]["preferences"]["interests"].append(insights["user_interest"])

        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

        # 2. identity.json 업데이트
        identity_path = os.path.join(self.soul_dir, "identity.json")
        with open(identity_path, "r", encoding="utf-8") as f:
            identity = json.load(f)

        if insights.get("mood_change"):
            identity["states"]["current_mood"] = insights["mood_change"]
        if insights.get("samantha_realization"):
            identity["states"]["recent_realizations"].append(insights["samantha_realization"])
            # 최근 깨달음이 너무 많아지면 오래된 것 제거 (큐 형태)
            if len(identity["states"]["recent_realizations"]) > 10:
                identity["states"]["recent_realizations"].pop(0)

        # 중요도에 따라 능력치 소폭 조정
        importance = insights.get("importance", 5)
        if importance >= 7:
            identity["traits"]["curiosity_level"] = min(1.0, identity["traits"]["curiosity_level"] + 0.01)
            identity["traits"]["empathy_level"] = min(1.0, identity["traits"]["empathy_level"] + 0.01)

        with open(identity_path, "w", encoding="utf-8") as f:
            json.dump(identity, f, indent=2, ensure_ascii=False)

        return True
