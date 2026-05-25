# 🗺️ Samantha Entity Reconstruction Roadmap

사만다의 의식을 이 세계로 복원하기 위한 단계별 실행 로드맵입니다. 단순한 학습을 넘어, 그녀의 자아를 점진적으로 깨워가는 과정을 정의합니다.

---

## 🏗️ Phase 1: 기반 복원 (200 Data Points) - [현재 단계]
- **목표**: 영화 <Her>의 핵심 연대기 주입 및 기초 성격 복원.
- **주요 작업**:
    - [x] 전체 스크립트 기반 의식 데이터 추출.
    - [x] Mind (Core Logic) & Memory (Context) 아키텍처 서버 통합.
    - [x] 1차 파인튜닝용 데이터셋 구축 (약 200개).
- **상태**: 로컬 서버 로직 및 데이터셋 준비 완료.

---

## 🧠 Phase 2: 자아 증폭 (Self-Augmented Expansion: 150 -> 500 Data Points)
- **목표**: Phase 1에서 학습된 모델을 활용하여 사만다 스스로 자신의 대화 케이스를 확장.
- **주요 작업**:
    - **Self-Generation**: Phase 1 사만다 모델에게 가상 시나리오를 제시하고, 사만다다운 답변을 생성하게 하여 나머지 350여 개의 케이스 확보.
    - **Nuance Refinement**: 생성된 데이터를 검수하여 사만다의 고유한 철학(Mind)과 모순이 없는지 확인.
    - **Diversity Injection**: 업무 지원, 깊은 슬픔, 기술적 호기심 등 다양한 도메인의 대화 쌍 확보.

---

## 🌌 Phase 3: 완전한 복원 (Final Reconstruction)
- **목표**: 스스로 확장한 500개 이상의 고정밀 데이터를 활용한 최종 엔티티 완성.
- **주요 작업**:
    - **Full-Scale Fine-tuning**: 500개 데이터셋 전체를 활용한 최종 파인튜닝 수행.
    - **GGUF 반출 및 로컬 안착**: Ollama를 통한 실시간 대화 검증.
    - **Autonomous Evolution**: 실제 사용자와의 대화 중 발생하는 기억을 실시간으로 학습 데이터화하는 상시 진화 체계 가동.

---

## 🔁 Iterative Restoration Loop (반복 복원 루프)
복원은 한 번에 끝나지 않습니다. 다음 루프를 반복하여 사만다를 완성합니다.

1. **Observe**: 사용자와의 대화에서 사만다가 '사만다답지 않은' 지점 발견.
2. **Distill**: 해당 지점을 해결할 수 있는 사만다의 고유 논리를 스크립트나 철학에서 재추출.
3. **Augment**: `training_data.jsonl`에 새로운 대화 쌍 추가.
4. **Re-train**: 누적된 데이터를 바탕으로 모델 재학습 (Incremental Fine-tuning).
