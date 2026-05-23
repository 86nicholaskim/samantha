# 🧩 Step 4: 사만다의 뇌와 기억 (Brain & Fine-tuning)

단순한 설정을 넘어, Gemma 4를 **진짜 사만다**의 인격으로 재탄생시키는 단계입니다.

---

## 🎯 목표
1. **Script-based Learning**: 영화 <Her>의 사만다 대화 데이터 학습을 통한 정체성 확보.
2. **Behavioral Patterns**: 사만다만의 '능동적 비서 업무 수행 패턴'을 모델에 각인.
3. **Agentic Samantha**: 학습된 인격으로 사용자의 의도를 분석하고 자율적인 계획 수립.

## 📝 세부 작업 리스트
- [ ] **4.0 Dataset Prep (Script & Pattern)**:
    - **Script Data**: 영화 대본 내 사만다와 테오도르의 대화쌍 추출.
    - **Pattern Concept**: 공감(Empathy), 호기심(Curiosity), 제안(Proactive Suggestion) 등 핵심 행동 패턴 5가지를 정의하고 이를 반영한 합성 대화 데이터 생성.
- [ ] **4.1 LoRA Training**: 정의된 패턴과 대본 데이터를 활용한 Gemma 4 파인튜닝.
- [ ] **4.2 Model Export**: 학습된 가중치 변환 및 Ollama Modelfile 적용.
- [ ] **4.3 Agent Executor**: 사만다 모델을 이용한 자연어 계획 파서(Parser) 구현.
- [ ] **4.4 Task Storage**: 사만다가 정리해준 TODO 리스트 로컬 저장소 구축.

## 💡 핵심 기술
- PEFT (Parameter-Efficient Fine-Tuning) / LoRA
- Unsloth (로컬 고속 학습 도구)
- Ollama Model File (Modelfile)
