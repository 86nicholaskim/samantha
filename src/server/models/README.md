# 🤖 Models & AI Engines

## 1. 개요
본 디렉토리는 사만다의 '지능'을 담당하는 AI 모델과의 인터페이스를 관리합니다.

## 2. 현재 사용 중인 모델
- **Base Model**: `gemma4:e4b` (Ollama)
- **Role**: 기본 대화 및 메모리 증류(Distillation) 수행.

## 3. 모델 진화 로드맵
현재는 기본 모델을 사용하고 있으나, 향후 사만다 전용 파인튜닝 모델로 교체될 예정입니다.

1. **Phase 1**: `gemma4:e4b` (System Prompt 기반 페르소나 주입)
2. **Phase 2**: `gemma4:samantha` (LoRA 파인튜닝된 전용 모델)

## 4. 파인튜닝 및 배포 프로세스
사만다 전용 모델을 생성하고 적용하는 과정은 다음과 같습니다:
1. **데이터 준비**: `/soul/samantha_train_dataset.jsonl` 업데이트.
2. **클라우드 학습**: Google Colab + Unsloth를 이용한 QLoRA 학습.
3. **모델 반출**: 학습된 모델을 GGUF 형식으로 변환.
4. **로컬 등록**: Ollama에 신규 모델 등록.
5. **설정 변경**: `src/server/config/settings.py`의 `MODEL_NAME` 수정.

> 📝 상세 전략 문서: [Training Hub](../../../doc/training/README.md)

## 5. 주요 컴포넌트
- `ollama_client.py`: Ollama API와의 통신을 담당하는 클라이언트 클래스.
