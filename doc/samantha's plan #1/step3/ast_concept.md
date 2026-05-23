# 🌳 Lexical AST 개념

> AST(Abstract Syntax Tree) — 에디터 내용을 트리 구조로 표현한 것

---

## 왜 AST인가?

Lexical은 에디터 내용을 **DOM이 아닌 자체 트리 구조**로 관리합니다.
이 트리가 `EditorState` 내부의 AST입니다.

- DOM은 렌더링 결과물 → 직접 조작하면 불안정
- AST는 순수한 데이터 → 직렬화/복원/비교가 안전

---

## 트리 구조

```
RootNode                        ← EditorState 최상위, 항상 1개
├── HeadingNode (tag: h1)       ← ## 입력 시 생성
│   └── TextNode ("제목")
├── ParagraphNode               ← 기본 단락
│   └── TextNode (format: bold)
└── TableNode                   ← 테이블 컨테이너
    └── TableRowNode            ← 행 (row)
        └── TableCellNode       ← 셀 (cell)
            └── TextNode ("내용")
```

### 노드 분류

| 노드 | 역할 | 등록 패키지 |
|---|---|---|
| `RootNode` | 최상위, 자동 생성 | 기본 내장 |
| `HeadingNode` | h1~h6 제목 | `@lexical/rich-text` |
| `QuoteNode` | 인용문 | `@lexical/rich-text` |
| `ParagraphNode` | 기본 단락 | 기본 내장 |
| `ListNode` | 리스트 컨테이너 | `@lexical/list` |
| `ListItemNode` | 리스트 항목 | `@lexical/list` |
| `CodeNode` | 코드 블록 | `@lexical/code` |
| `TableNode` | 테이블 컨테이너 | `@lexical/table` |
| `TableRowNode` | 테이블 행 | `@lexical/table` |
| `TableCellNode` | 테이블 셀 | `@lexical/table` |
| `TextNode` | 실제 텍스트 | 기본 내장 |

---

## toJSON() — AST 직렬화

`EditorState.toJSON()`을 호출하면 AST를 JSON으로 직렬화합니다.

```json
{
  "root": {
    "type": "root",
    "children": [
      {
        "type": "heading",
        "tag": "h1",
        "children": [
          { "type": "text", "text": "제목", "format": 0 }
        ]
      },
      {
        "type": "table",
        "children": [
          {
            "type": "tablerow",
            "children": [
              {
                "type": "tablecell",
                "children": [
                  { "type": "text", "text": "셀 내용" }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

이 JSON을 저장하면 나중에 `editor.parseEditorState(json)`으로 완벽히 복원됩니다.

---

## MobX 연결 흐름

```
사용자 입력
    ↓
Lexical EditorState 업데이트
    ↓
registerUpdateListener 발동
    ↓
editorState.toJSON()  →  editorStore.setAST(ast)
    ↓
MobX observable 상태 변경
    ↓                         ↓
Toolbar (observer)      PrintPlugin
버튼 활성화/비활성화    $generateHtmlFromNodes()
                              ↓
                         iframe → 인쇄
```

### 핵심 코드

```typescript
// EditorStatePlugin.tsx
editor.registerUpdateListener(({ editorState }) => {
  editorStore.setAST(editorState.toJSON());
});

// editorStore.ts
get hasContent(): boolean {
  return this.docAST?.root?.children?.length > 0;
}

// Toolbar.tsx (observer로 감싸야 반응함)
const Toolbar = observer(() => (
  <button disabled={!editorStore.hasContent}>인쇄</button>
));
```

---

## 핵심 포인트

**노드 등록 없이는 변환 안 됨**
`MarkdownShortcutPlugin`이 `## `를 감지해도 `HeadingNode`가 `initialConfig.nodes`에 없으면 변환이 일어나지 않습니다.

**TableNode는 3개 세트**
`TableNode`, `TableRowNode`, `TableCellNode` — 하나라도 빠지면 런타임 에러.

**`$`로 시작하는 함수는 EditorState 컨텍스트 필요**
`$getRoot()`, `$generateHtmlFromNodes()` 등은 반드시 `editorState.read()` 또는 `editor.update()` 내부에서 호출해야 합니다.
