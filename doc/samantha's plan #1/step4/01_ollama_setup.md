# 🛠️ 4.1: Ollama 설치 및 로컬 AI 엔진 설정

이 문서는 외부 네트워크 트래픽 없이 로컬 PC의 자원(CPU/GPU)만을 활용하여 AI 에이전트를 구동하고, 이를 애플리케이션 내부에 통합하기 위한 기초 설정을 다룹니다.

---

## 1. Ollama 설치 및 환경 구성

Ollama는 로컬 환경에서 LLM을 가장 쉽고 효율적으로 서빙할 수 있는 엔진입니다.

### 설치 단계
1. **다운로드**: [Ollama 공식 홈페이지](https://ollama.com/)에서 OS에 맞는 설치 파일을 내려받아 설치합니다.
2. **설치 확인**: 터미널(PowerShell/CMD)에서 아래 명령어를 입력합니다.
   ```bash
   ollama --version
   ```
3. **Gemma 모델 로드**: Google의 가벼우면서 강력한 로컬 모델인 Gemma를 다운로드합니다.
   ```bash
   ollama pull gemma
   ```

---

## 2. 네트워크 독립성 설정 (No-Traffic AI)

애플리케이션이 외부 API(OpenAI, Gemini 등)를 호출하지 않고 로컬 Ollama와만 통신하도록 설정합니다.

- **기본 접속 주소**: `http://localhost:11434`
- **CORS 설정 (필요시)**: 프론트엔드에서 직접 Ollama에 접근해야 할 경우 환경 변수 설정이 필요합니다. (보통은 백엔드를 거치는 것을 권장)

---

## 3. 코딩 에이전트로 활용하기

설치된 Gemma 모델을 개발 중에 활용하는 방법입니다.

- **CLI 활용**: `ollama run gemma`를 통해 즉석에서 코드 로직 질문.
- **IDE 연동**: VS Code 확장 프로그램(예: Continue, Llama Coder)에서 로컬 Ollama 주소를 연결하여 자동 완성 및 리팩토링 에이전트로 사용.

---

## 4. 애플리케이션 내장형 AI (Embedded LLM)

우리가 만드는 웹 앱 안에서 Gemma를 엔진으로 사용하는 구조입니다.

1. **Backend Bridge**: Node.js(Express) 서버가 Ollama API와 통신하는 클라이언트 역할을 수행.
2. **Frontend Interface**: Lexical 에디터의 AST 데이터를 백엔드로 보내면, 백엔드가 로컬 Gemma에게 전달하여 가공된 결과(요약, 교정 등)를 다시 에디터에 주입.

---

## ✅ 준비 상태 체크리스트
- [ ] `ollama --version` 명령어가 정상 작동하는가?
- [ ] `ollama list`에 `gemma` 모델이 포함되어 있는가?
- [ ] `curl http://localhost:11434` 호출 시 "Ollama is running" 메시지가 나오는가?
