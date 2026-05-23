# 🧩 Step 3: Lexical 에디터 확장

> Markdown 단축키 + 테이블 + 인쇄 출력 기능 구현

이 단계에서는 베이스 에디터(`RichTextPlugin`만 있는 상태)에 실용적인 기능 3가지를 순서대로 추가합니다.

---

## 🎯 목표

| 기능 | 설명 |
| :--- | :--- |
| **Markdown Shortcut** | `## `, `**bold**`, `- ` 등 입력 시 자동 변환 |
| **Table** | 툴바에서 테이블 삽입, 셀 편집 |
| **인쇄 출력** | 에디터 영역만 iframe으로 분리하여 인쇄 |

---

## 🏗️ 구현 구조

```text
apps/frontend/src/
├── component/
│   ├── Editor.tsx          # LexicalComposer + 플러그인 조합
│   └── Toolbar.tsx         # 테이블 삽입 버튼 등 툴바 UI
├── plugin/
│   ├── TablePlugin.tsx     # 테이블 커맨드 처리
│   └── PrintPlugin.tsx     # 인쇄 트리거 + iframe 처리
└── store/
    └── editorStore.ts      # MobX: AST 상태 관리
```

---

## 🔄 데이터 흐름

```text
사용자 입력
    ↓
Lexical EditorState (AST)
    ↓
registerUpdateListener
    ↓
MobX editorStore.setAST()
    ↓
┌─────────────┬──────────────┐
│  Toolbar    │  PrintPlugin │
│  (상태 반영) │  (HTML 변환) │
└─────────────┴──────────────┘
```

---

## 📦 추가 패키지

```bash
pnpm add \
  @lexical/markdown@0.44.0 \
  @lexical/rich-text@0.44.0 \
  @lexical/list@0.44.0 \
  @lexical/code@0.44.0 \
  @lexical/table@0.44.0 \
  @lexical/html@0.44.0 \
  mobx \
  mobx-react-lite \
  print-js \
  --filter=frontend
```

---

## ✅ 구현 순서

1. **패키지 설치** → `setting.md` 참고
2. **노드 등록** → `Editor.tsx` `initialConfig.nodes` 배열에 추가
3. **플러그인 추가** → `MarkdownShortcutPlugin`, `TablePlugin`
4. **MobX 스토어** → `editorStore.ts` 생성
5. **툴바 UI** → `Toolbar.tsx` 테이블 삽입 버튼
6. **인쇄** → `PrintPlugin.tsx` iframe 방식

---

## 🔑 핵심 개념

### 노드 등록이 왜 필요한가?

Lexical은 **사용할 노드 타입을 명시적으로 등록**해야 합니다.
등록하지 않으면 플러그인을 붙여도 변환이 일어나지 않습니다.

```
HeadingNode   → ## 제목
ListNode      → - 목록
CodeNode      → ```코드```
TableNode     → 테이블
```

### MobX와 EditorState

Lexical의 EditorState는 내부적으로 AST(Abstract Syntax Tree) 구조입니다.
`toJSON()`으로 직렬화하면 MobX observable로 관리할 수 있고,
에디터 바깥의 컴포넌트(툴바, 인쇄 버튼)에서 이 상태를 구독할 수 있습니다.
