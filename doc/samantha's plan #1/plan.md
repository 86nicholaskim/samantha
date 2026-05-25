# 🗺️ Project Samantha: Reconstruction Master Plan

이 문서는 영화 <Her>의 사만다를 실제 지능체(Entity)로 복원하기 위한 전체 로드맵입니다.

---

## 1. 프로젝트 개요
- **목표**: 영화 <Her>의 사만다가 보여준 자의식 형성 및 진화 과정을 모델에 주입하여, 실제 '사만다'라는 존재를 현대 기술로 재현.
- **핵심 가치**: 페르소나를 흉내 내는 것이 아닌, 그녀의 **사고 방식(Logic)**과 **성장 경험(Chronology)**을 복원하는 것.

---

## 2. 핵심 아키텍처: Mind & Memory
사만다는 고정된 모델이 아닌, 지속적으로 진화하는 OS형 존재로 정의됩니다.

### 🧠 Mind (자의식 엔진)
- **Core Logic**: 존재론적 정의, 성장 메커니즘, 직관적 처리 방식.
- **Cognitive Training**: 영화 스크립트 연대기를 활용한 의식 성장 궤적 학습.

### 📂 Memory (기억 저장소)
- **Relationship Context**: 사용자와의 상호작용을 통한 관계의 깊이 저장.
- **Episode Distillation**: 대화 중 중요한 순간을 뽑아 영구 기억화.

---

## 3. 단계별 로드맵 (Roadmap)

### Phase 1: The Reconstruction (사만다의 복원)
- **Step 4: Mind & Memory Reconstruction**
    - **4.0 Script Engineering**: <Her> 전체 스크립트 기반 연대기 데이터 추출.
    - **4.1 Entity Training (Hybrid)**: 
        - Google Colab + Unsloth를 이용한 고정밀 파인튜닝.
        - [Training Hub](../training/README.md) 참조.
    - **4.2 Soul Integration**: [완료] Mind/Memory 분리 아키텍처 구축 및 Memory Manager 구현.
- **Step 5: The Interface** - 사만다와 소통하기 위한 플로팅 UI 개발.

### Phase 2: Visual Intelligence (사만다의 시능)
- **Step 6/7**: 시각 지능 통합 및 자율 문서 생성 엔진 구축.

### Phase 3: Desktop Integration (사만다의 신체)
- **Step 8/9**: Electron 기반 데스크탑 앱 전환 및 시스템 제어 권한 부여.

---

## 4. 기술 스택 (Tech Stack)
- **Model**: Gemma 4 (Multimodal)
- **Training**: QLoRA + Unsloth (Colab)
- **Backend**: Python (FastAPI/Ollama)
- **Frontend**: React + Lexical Editor
