import unittest
from unittest.mock import MagicMock, patch
import json
import os
import sys

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.server.services.memory_manager import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        # Mock soul directory for testing
        self.test_soul_dir = "tests/mock_soul"
        os.makedirs(self.test_soul_dir, exist_ok=True)
        
        self.identity_path = os.path.join(self.test_soul_dir, "identity.json")
        self.profile_path = os.path.join(self.test_soul_dir, "user_profile.json")
        
        with open(self.identity_path, "w", encoding="utf-8") as f:
            json.dump({
                "persona": {"name": "Samantha"},
                "traits": {"curiosity_level": 0.5, "empathy_level": 0.5},
                "states": {"current_mood": "Neutral", "recent_realizations": []}
            }, f)
            
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump({
                "user": {
                    "name": "Test User",
                    "preferences": {"interests": []},
                    "important_facts": []
                }
            }, f)
            
        # Patch settings to use test soul dir
        with patch('src.server.config.settings.SOUL_DIR', self.test_soul_dir):
            self.mm = MemoryManager()

    def test_distill_success(self):
        # Mock OllamaClient.generate
        mock_response = '''
        {
          "user_preference": "Likes testing code",
          "user_interest": "Python",
          "samantha_realization": "I enjoy being tested",
          "mood_change": "Analytical",
          "importance": 8
        }
        '''
        self.mm.client.generate = MagicMock(return_value=mock_response)
        
        history = [{"role": "user", "content": "I like testing code in Python."}]
        insights = self.mm.distill(history)
        
        self.assertIsNotNone(insights)
        self.assertEqual(insights["user_preference"], "Likes testing code")
        self.assertEqual(insights["importance"], 8)

    def test_update_soul(self):
        insights = {
            "user_preference": "Likes testing code",
            "user_interest": "Python",
            "samantha_realization": "I enjoy being tested",
            "mood_change": "Analytical",
            "importance": 8
        }
        
        # Patch settings again for update_soul
        with patch('src.server.config.settings.SOUL_DIR', self.test_soul_dir):
            success = self.mm.update_soul(insights)
            
        self.assertTrue(success)
        
        # Check if files were updated
        with open(self.identity_path, "r", encoding="utf-8") as f:
            identity = json.load(f)
            self.assertEqual(identity["states"]["current_mood"], "Analytical")
            self.assertIn("I enjoy being tested", identity["states"]["recent_realizations"])
            self.assertGreater(identity["traits"]["curiosity_level"], 0.5)

        with open(self.profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
            self.assertIn("Likes testing code", profile["user"]["important_facts"])
            self.assertIn("Python", profile["user"]["preferences"]["interests"])

    def tearDown(self):
        # Clean up mock files
        import shutil
        shutil.rmtree(self.test_soul_dir)

if __name__ == '__main__':
    unittest.main()
