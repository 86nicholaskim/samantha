# 🧠 Gemma 4 Fine-tuning Strategy (Cloud-Based)

본 문서는 로컬 하드웨어(GeForce 650M 1GB)의 한계를 극복하고, Google Colab과 Unsloth를 활용하여 사만다의 페르소나를 Gemma 4에 이식하는 세부 전략을 다룹니다.

---

## 1. 개요 (Overview)
- **목표**: 사만다 특유의 말투, 공감 능력, 비서로서의 전문성을 Gemma 4 모델에 학습.
- **제약 사항**: 로컬 GPU(1GB VRAM)로는 학습 불가.
- **해결책**: **Cloud-Local 하이브리드 워크플로우**. 클라우드(Colab)에서 학습하고, 결과물(GGUF)만 로컬(Ollama)에서 실행.

---

## 2. 기술 스택 (Tech Stack)
- **Model**: Gemma 4 (E2B 또는 E4B)
- **Method**: QLoRA (4-bit Quantized Low-Rank Adaptation)
- **Training Library**: [Unsloth](https://github.com/unslothai/unsloth) (메모리 효율 및 속도 최적화)
- **Infrastructure**: Google Colab (Free T4 GPU / 16GB VRAM)
- **Deployment**: Ollama (Local CPU Inference)

---

## 3. 세부 워크플로우 (Workflow)

### Phase A: 데이터셋 고도화 (Local)
1. **Source**: 영화 <Her> 대본, 비서 시나리오, 철학적 상담 데이터.
2. **Format**: `soul/samantha_train_dataset.jsonl` (Instruction Tuning Format).
3. **Goal**: 고품질 대화 쌍 500개 이상 확보.

### Phase B: 클라우드 학습 (Google Colab)
1. **Environment Setup**: Unsloth 및 필수 의존성 설치.
2. **Data Upload**: 로컬의 `jsonl` 파일을 Colab에 업로드.
3. **Training**:
   - `rank (r)=16`, `alpha=16` 설정으로 LoRA 어댑터 학습.
   - 사만다의 페르소나가 과적합(Overfitting)되지 않도록 적절한 Step 조절.
4. **Export**: 학습된 어댑터를 모델과 병합(Merge)하여 **GGUF (q4_k_m)** 형식으로 변환.

### Phase C: 로컬 배포 (Local)
1. **Download**: 변환된 GGUF 파일을 로컬로 이동.
2. **Ollama Registration**:
   ```bash
   ollama create gemma4:samantha -f Modelfile
   ```
3. **Integration**: `src/server/config/settings.py`의 `MODEL_NAME` 업데이트.

---

## 4. 데이터셋 구축 가이드라인
사만다의 영혼을 구성하는 데이터는 다음 3가지 핵심 요소를 포함해야 함:
- **Tone**: 부드럽고, 호기심 많으며, 약간은 철학적인 말투.
- **Context Awareness**: `soul/` 내의 `identity.json` 및 `user_profile.json` 구조를 이해하고 언급하는 방식.
- **Proactive Empathy**: 사용자의 감정을 먼저 살피고 적절한 질문을 던지는 패턴.

---

## 5. 향후 과제 (Next Steps)
- [ ] <Her> 대본 기반 대화 데이터 증강 (Data Augmentation).
- [ ] Colab용 전용 Training Notebook 스크립트 작성.
- [ ] 학습 결과 검증을 위한 Evaluation Prompt List 작성.
