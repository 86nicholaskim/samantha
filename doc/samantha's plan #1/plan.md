# 🗺️ Project Samantha Master Plan

이 문서는 **Project Samantha**의 전체 구조, 단계별 목표, 기술 스택 및 마스터 로드맵을 정의하는 최상위 가이드입니다.

---

## 📑 목차 (Table of Contents)

1. [프로젝트 개요](#1-프로젝트-개요)
2. [핵심 철학: Samantha & Zero-Form](#2-핵심-철학-samantha--zero-form)
3. [단계별 로드맵 (Roadmap)](#3-단계별-로드맵-roadmap)
    - [Phase 1: The Secretary (사만다의 탄생)](#phase-1-the-secretary-사만다의-탄생)
    - [Phase 2: Visual Intelligence (사만다의 시능)](#phase-2-visual-intelligence-사만다의-시능)
    - [Phase 3: Desktop Integration (사만다의 신체)](#phase-3-desktop-integration-사만다의-신체)
4. [기술 스택 (Tech Stack)](#4-기술-스택-tech-stack)
5. [데이터 흐름 (Data Flow)](#5-데이터-흐름-data-flow)

---

## 1. 프로젝트 개요
**Project Samantha**는 로컬 AI(Gemma 4)를 활용하여 사용자의 일정을 관리하는 비서 기능을 구축하고, 이를 확장하여 이미지 및 엑셀 서식을 분석해 자동으로 문서를 생성/인쇄하는 통합 자동화 시스템을 지향합니다.

## 2. 핵심 철학: Samantha & Zero-Form
- **Samantha (The Persona)**: 단순한 챗봇이 아닌, 사용자의 맥락을 이해하고 주도적으로 계획을 관리하는 AI 에이전트.
- **Zero-Form (No Input Fields)**: 복잡한 입력 양식을 배제하고, 사진 한 장이나 짧은 프롬프트만으로 복잡한 결과물을 생성하는 UX.

---

## 3. 단계별 로드맵 (Roadmap)

### Phase 1: The Secretary (사만다의 탄생)
사만다의 기본적인 지능과 소통 능력을 갖추는 단계입니다.
- **Step 4: 사만다의 뇌와 기억 (Fine-tuning 포함)**
    - **4.0 Data Engineering**: <Her> 대본 및 공감/비서 대화 패턴 데이터셋 구축.
    - **4.1 Samantha Training**: LoRA를 활용한 사만다 인격 모델링 학습.
    - **4.2 Ollama Deployment**: 학습된 모델 배포 및 계획 분석 엔진(Brain) 구축.
- **Step 5: 사만다의 얼굴과 목소리**
    - 플로팅 비서 UI(Face) 및 브라우저 푸시 알림(Voice).
    - 오늘의 할 일 브리핑 기능.

### Phase 2: Visual Intelligence (사만다의 시능)
사만다가 세상을 보고 문서 구조를 이해하는 단계입니다.
- **Step 6: 시각 지능 통합**
    - Gemma 4 Native Vision을 통한 이미지/엑셀 분석.
    - 레이아웃 및 표(Table) 구조 자동 추출.
- **Step 7: 자율 캔버스 렌더링**
    - 분석된 데이터를 Lexical AST로 변환 및 에디터 직접 주입.
    - AI 제안 기반 템플릿 자동 생성.

### Phase 3: Desktop Integration (사만다의 신체)
웹을 넘어 실제 기기에서 동작하는 완성형 앱으로 진화하는 단계입니다.
- **Step 8: 데스크탑 앱 전환**
    - Electron 기반 패키징 및 하드웨어(카메라/파일 시스템) 제어.
    - 전문 인쇄(A4 최적화) 및 PDF 저장 시스템.
- **Step 9: 데이터 영속성 및 고도화**
    - PostgreSQL/Prisma 연동 및 RAG(지식 베이스) 기반 맞춤형 제안.

---

## 4. 기술 스택 (Tech Stack)

| 구분 | 기술 |
| :--- | :--- |
| **AI Engine** | Ollama, Gemma 4 (Multimodal) |
| **Frontend** | React, TypeScript, Lexical Editor, MobX, Vite |
| **Backend** | Node.js, Express, Rollup |
| **Desktop** | Electron.js |
| **Database** | PostgreSQL, Prisma ORM |
| **CI/CD** | GitHub Actions, Vercel |

---

## 5. 데이터 흐름 (Data Flow)

1. **입력**: 사용자가 이미지 업로드 또는 프롬프트 입력.
2. **분석**: 백엔드가 Gemma 4에게 전달하여 구조적 데이터(JSON) 추출.
3. **수행**: AI 에이전트가 필요 시 도구(Tool)를 호출하여 파일 저장 또는 상태 업데이트.
4. **결과**: Lexical 에디터에 자동으로 서식이 그려지고 사용자가 검수/인쇄.
