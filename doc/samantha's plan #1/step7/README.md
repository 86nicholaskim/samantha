# 🧩 Step 7: 자율 캔버스 렌더링 (Canvas & Template)

사만다가 분석한 정보를 **Lexical 에디터에 자동으로 그리는** 단계입니다.

---

## 🎯 목표
1. **AST 직접 주입**: AI의 분석 결과를 Lexical의 추상 구문 트리(AST)로 변환.
2. **템플릿 자동 생성**: 사진 속 서식과 99% 유사한 HTML/CSS 템플릿 생성.
3. **편집 및 보정**: AI가 그린 결과물을 사용자가 즉시 수정할 수 있는 워크플로우.

## 📝 세부 작업 리스트
- [ ] **7.1 AST Mapper**: AI JSON 데이터를 Lexical Node 구조로 매핑.
- [ ] **7.2 Template Generator**: 인쇄에 최적화된 HTML/CSS 템플릿 자동 생성.
- [ ] **7.3 Canvas Sync**: AI가 에디터 내부 내용을 직접 업데이트하는 기능.
- [ ] **7.4 Review Flow**: AI 결과물에 대한 사용자 최종 승인 인터페이스.

## 💡 핵심 기술
- Lexical Editor AST Manipulation
- Dynamic HTML/CSS Rendering
- JSON-to-AST Mapping
