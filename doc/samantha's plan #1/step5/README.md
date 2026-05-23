# 🧩 Step 5: 사만다의 얼굴과 목소리 (Face & Voice)

사만다가 사용자에게 정보를 보여주고 **알림**을 주는 인터페이스 단계입니다.

---

## 🎯 목표
1. **미니멀 UI**: 에디터 방해 없이 소통하는 전용 비서 창 구현.
2. **실시간 리마인더**: 약속된 시간에 시스템 알림(Notification) 발생.
3. **상태 보고**: 현재 프로젝트의 진척도를 요약해서 보고하는 브리핑 기능.

## 📝 세부 작업 리스트
- [ ] **5.1 Assistant UI**: 프론트엔드 우측 하단 플로팅 비서 패널 개발.
- [ ] **5.2 Notification API**: 브라우저 및 OS 레벨 알림 연동.
- [ ] **5.3 Real-time Sync**: 백엔드와 프론트엔드 간의 상태 동기화 (SSE/WS).
- [ ] **5.4 Progress Briefing**: `TODO.md`를 읽어 오늘의 할 일을 요약해주는 로직.

## 💡 핵심 기술
- Browser Notification API
- React Portal (Floating UI)
- Server-Sent Events (SSE)
