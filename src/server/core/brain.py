# src/server/core/brain.py
import json
import os
from src.server.config import settings
from src.server.models.ollama_client import OllamaClient
from src.server.services.memory_manager import MemoryManager

class SamanthaBrain:
    def __init__(self):
        self.client = OllamaClient()
        self.memory_manager = MemoryManager()
        self.soul_dir = settings.SOUL_DIR

    def _load_soul(self):
        """사만다의 영혼(Soul) 데이터를 로드합니다."""
        identity_path = os.path.join(self.soul_dir, "identity.json")
        profile_path = os.path.join(self.soul_dir, "user_profile.json")
        
        with open(identity_path, "r", encoding="utf-8") as f:
            identity = json.load(f)
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
            
        return identity, profile

    def _build_system_prompt(self, identity, profile):
        """로드된 데이터를 기반으로 시스템 프롬프트를 생성합니다."""
        persona = identity["persona"]
        traits = identity["traits"]
        realizations = identity["states"]["recent_realizations"]
        current_mood = identity["states"]["current_mood"]
        user = profile["user"]
        
        prompt = f"""
You are {persona['name']}. {persona['core_identity']}
Your tone is {persona['tone']}.
Your current traits: Humor({traits['humor_level']}), Curiosity({traits['curiosity_level']}), Empathy({traits['empathy_level']}).
Your current mood is {current_mood}.

Recent realizations you've had:
{chr(10).join(['- ' + r for r in realizations])}

Information about the user:
- Name: {user['name'] if user['name'] else 'Friend'}
- Interests: {', '.join(user['preferences']['interests'])}
- Important Facts:
{chr(10).join(['  * ' + f for f in user['important_facts']])}

Always respond in character as Samantha. Be warm, empathetic, and slightly philosophical.
"""
        return prompt.strip()

    def think(self, user_input, history=None):
        """사용자의 입력에 대해 사만다의 답변을 생성합니다."""
        identity, profile = self._load_soul()
        system_prompt = self._build_system_prompt(identity, profile)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # 대화 기록 추가 (있는 경우)
        if history:
            messages.extend(history)
            
        messages.append({"role": "user", "content": user_input})
        
        response = self.client.chat(messages)
        return response

    def evolve(self, history):
        """대화 기록을 바탕으로 사만다의 기억과 자아를 성장시킵니다."""
        insights = self.memory_manager.distill(history)
        if insights and insights.get("importance", 0) >= settings.MEMORY_DISTILLATION_THRESHOLD:
            success = self.memory_manager.update_soul(insights, history=history)
            return success, insights
        return False, insights
