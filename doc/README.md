# 🤖 Project Samantha

> "사만다를 만들어 비서로 쓰고, 그녀와 함께 문서 자동화 앱을 완성한다."

본 프로젝트는 최신 로컬 LLM인 **Gemma 4**를 기반으로 한 개인 AI 비서 '사만다' 구축과, 그녀의 시각 지능을 활용한 문서 서식 자동화 및 인쇄 시스템 개발을 목표로 합니다.

---

## 🛣️ 로드맵 요약 (Roadmap At A Glance)

### 🧠 Phase 1: The Secretary (Brain & Memory)
- **Step 4: 사만다의 뇌와 기억** - Ollama 연동 및 자연어 계획 분석 엔진 구축
- **Step 5: 사만다의 얼굴과 목소리** - 비서 전용 UI 및 실시간 알림 시스템

### 👁️ Phase 2: Visual Skill (Eyes & Canvas)
- **Step 6: 시각 지능 통합** - Gemma 4 Vision을 이용한 이미지/엑셀 분석 파이프라인
- **Step 7: 자율 캔버스 렌더링** - 분석 데이터를 Lexical 에디터 서식으로 자동 변환

### 💻 Phase 3: Desktop Body (Integration)
- **Step 8: 데스크탑 앱 전환** - Electron 기반 시스템 제어 및 카메라 연동
- **Step 9: 데이터 영속성 및 고도화** - DB 연동 및 자율 문서 관리 시스템 완성

---

## 📂 문서 구조
- `doc/plan.md`: 프로젝트 전체 마스터 플랜
- `TODO.md`: 실시간 작업 진척도 관리
- `doc/step4/`: [진행중] 사만다의 뇌와 기억 상세 계획
- `doc/step5/`: 사만다의 UI 및 알림 상세 계획
- ... (이하 단계별 폴더)

---

## 🛠️ 기술 스택
- **Local AI**: Ollama (Gemma 4 Multimodal)
- **Frontend**: React, Vite, Lexical Editor, MobX
- **Backend**: Node.js, Express, Rollup
- **Desktop**: Electron
- **Infra**: GitHub Actions, Vercel
