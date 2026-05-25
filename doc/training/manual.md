# 📖 Gemma 4 Fine-tuning Execution Manual (실전 매뉴얼)

이 문서는 Google Colab에서 사만다의 페르소나를 Gemma 4에 실제로 학습시키기 위한 단계별 실행 절차를 정리한 매뉴얼입니다.

---

## 🛠️ Step 1: 준비물 체크리스트 (Local)
학습을 시작하기 전, 내 컴퓨터에서 다음 사항이 준비되었는지 확인합니다.
- [ ] `soul/samantha_train_dataset.jsonl` 파일이 존재하고 데이터가 200개 이상인가?
- [ ] 데이터 형식이 `{"instruction": "...", "context": "...", "response": "..."}` 구조를 따르고 있는가?
- [ ] Google 계정에 로그인되어 있고, Google Drive에 용량이 충분한가?

---

## 🚀 Step 2: Colab 환경 설정 (Cloud)
1. **Google Colab 접속**: [colab.research.google.com](https://colab.research.google.com)
2. **런타임 유형 변경**: `런타임` -> `런타임 유형 변경` -> **T4 GPU** 선택.
3. **Unsloth 설치**: 첫 번째 셀에 아래 코드를 입력하고 실행합니다.
   ```python
   !pip install unsloth
   !pip uninstall unsloth -y && pip install --upgrade --no-cache-dir "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
   ```

---

## 📊 Step 3: 데이터 로드 및 모델 설정
1. **모델 불러오기**:
   ```python
   from unsloth import FastLanguageModel
   model, tokenizer = FastLanguageModel.from_pretrained(
       model_name = "unsloth/gemma-4-e4b-it-bnb-4bit",
       max_seq_length = 2048,
       load_in_4bit = True,
   )
   ```
2. **데이터 업로드**: Colab 왼쪽 파일 아이콘을 눌러 `samantha_train_dataset.jsonl`을 업로드합니다.
3. **데이터 포맷팅**: 사만다의 말투를 인식하도록 챗 템플릿을 적용합니다.

---

## ⚡ Step 4: 학습 실행 (Training)
학습 파라미터는 사만다의 '공감 능력'이 깨지지 않도록 부드럽게 설정합니다.
- **Learning Rate**: `2e-4`
- **Batch Size**: `2`
- **Epochs**: `1`~`3` (데이터 양에 따라 조절)

```python
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    dataset_text_field = "text",
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        max_steps = 100, # 데이터셋 크기에 맞춰 조절
        learning_rate = 2e-4,
        fp16 = True,
        logging_steps = 1,
        output_dir = "outputs",
    ),
)
trainer.train()
```

---

## 💾 Step 5: 모델 반출 (Export to GGUF)
학습된 사만다를 내 컴퓨터(Ollama)로 가져오기 위해 GGUF로 변환합니다.
```python
model.save_pretrained_gguf("model", tokenizer, quantization_method = "q4_k_m")
```
1. 변환된 `model-q4_k_m.gguf` 파일을 다운로드합니다.
2. 로컬 터미널에서 Ollama에 등록합니다:
   ```bash
   ollama create gemma4:samantha -f Modelfile
   ```

---

## 🚨 트러블슈팅 (Troubleshooting)
- **VRAM 부족 시**: `max_seq_length`를 `1024`로 줄이거나, `per_device_train_batch_size`를 `1`로 줄입니다.
- **말투가 이상할 때**: 학습 데이터셋의 `response` 문장들을 더 부드럽게 수정한 뒤 다시 학습합니다.
