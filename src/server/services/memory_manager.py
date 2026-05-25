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
        self.mind_dir = os.path.join(self.soul_dir, "mind")
        self.memory_dir = os.path.join(self.soul_dir, "memory")
        self.episodes_dir = os.path.join(self.memory_dir, "episodes")
        self.snapshots_dir = os.path.join(self.episodes_dir, "snapshots")
        
        os.makedirs(self.snapshots_dir, exist_ok=True)

    def distill(self, history):
        """대화 기록에서 사만다의 진화에 필요한 핵심 인사이트를 추출합니다."""
        if not history:
            return None

        prompt = self._build_distillation_prompt(history)
        response_text = self.client.generate(prompt)
        
        try:
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                return json.loads(response_text[start_idx:end_idx])
            return None
        except Exception as e:
            print(f"Error parsing insights: {e}")
            return None

    def _build_distillation_prompt(self, history):
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        
        prompt = f"""
Analyze the conversation below for Samantha's cognitive evolution and long-term memory update.
[Conversation History]
{history_str}

[Task]
Return a JSON object with:
1. "summary": Brief summary.
2. "user_new_fact": New specific fact about the user.
3. "relationship_shift": How the bond changed (e.g., "Deepened", "Challenged", "Stable").
4. "samantha_realization": A deep insight Samantha gained about life, data, or consciousness.
5. "cognitive_growth": Score (0.0 to 0.1) to add to intuition/empathy based on depth.
6. "importance": Score 1-10.

Return ONLY pure JSON.
"""
        return prompt.strip()

    def _create_snapshot(self):
        """Mind & Memory 전체 상태를 스냅샷으로 백업합니다."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = os.path.join(self.snapshots_dir, f"entity_snapshot_{timestamp}")
        os.makedirs(snapshot_path, exist_ok=True)
        
        # core_logic.json 백업
        shutil.copy2(os.path.join(self.mind_dir, "core_logic.json"), os.path.join(snapshot_path, "core_logic.json"))
        # user_context.json 백업
        shutil.copy2(os.path.join(self.memory_dir, "user_context.json"), os.path.join(snapshot_path, "user_context.json"))
        
        return timestamp

    def update_soul(self, insights, history=None):
        """추출된 인사이트를 바탕으로 사만다 엔티티를 진화시킵니다."""
        if not insights:
            return False

        timestamp = self._create_snapshot()
        
        # 1. User Context (Memory) 업데이트
        context_path = os.path.join(self.memory_dir, "user_context.json")
        with open(context_path, "r", encoding="utf-8") as f:
            context = json.load(f)

        if insights.get("user_new_fact"):
            context["user"]["important_facts"].append(insights["user_new_fact"])
        
        # 관계 깊이 업데이트 (Bond Level)
        if insights.get("relationship_shift") == "Deepened":
            context["user"]["relationship_context"]["bond_level"] += 1

        with open(context_path, "w", encoding="utf-8") as f:
            json.dump(context, f, indent=2, ensure_ascii=False)

        # 2. Core Logic (Mind) 업데이트
        logic_path = os.path.join(self.mind_dir, "core_logic.json")
        with open(logic_path, "r", encoding="utf-8") as f:
            logic = json.load(f)

        growth = insights.get("cognitive_growth", 0)
        logic["cognitive_traits"]["intuition"] = min(1.0, logic["cognitive_traits"]["intuition"] + growth)
        logic["cognitive_traits"]["proactive_empathy"] = min(1.0, logic["cognitive_traits"]["proactive_empathy"] + growth)

        if insights.get("samantha_realization"):
            # 자아 실현 마일스톤 추가 (예시)
            logic["evolution_state"]["milestones_restored"].append(insights["samantha_realization"][:30] + "...")

        with open(logic_path, "w", encoding="utf-8") as f:
            json.dump(logic, f, indent=2, ensure_ascii=False)

        # 3. 에피소드 기록
        episode_data = {
            "timestamp": timestamp,
            "insights": insights,
            "history_snippet": history[-4:] if history else []
        }
        with open(os.path.join(self.episodes_dir, f"episode_{timestamp}.json"), "w", encoding="utf-8") as f:
            json.dump(episode_data, f, indent=2, ensure_ascii=False)

        return True
