# src/server/config/settings.py
import os

# Ollama 설정
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma4:e4b")

# 사만다 영혼(Soul) 경로 설정
# 프로젝트 루트의 soul 디렉토리를 참조합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SOUL_DIR = os.path.join(BASE_DIR, "soul")

# API 설정
API_HOST = "0.0.0.0"
API_PORT = 8000

# 대화 증류 설정
MEMORY_DISTILLATION_THRESHOLD = 7  # 1-10 점수 중 7점 이상일 때만 영구 기억화
