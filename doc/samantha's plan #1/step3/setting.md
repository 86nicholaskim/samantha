# 🛠️ Step 3: Lexical 에디터 확장 구축 가이드

각 블록의 내용을 해당 파일명으로 저장하세요.

---

## 1. 패키지 설치

```bash
# 버전을 기존 lexical@0.44.0 에 맞춰 고정 설치
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

# print-js 타입
pnpm add -D @types/print-js --filter=frontend
```

---

## 2. MobX 스토어 생성

📄 `apps/frontend/src/store/editorStore.ts`

```typescript
import { makeAutoObservable } from 'mobx';
import type { SerializedEditorState } from 'lexical';

class EditorStore {
  // 에디터 AST 상태 (Lexical EditorState의 직렬화 결과)
  docAST: SerializedEditorState | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  setAST(ast: SerializedEditorState) {
    this.docAST = ast;
  }

  // 파생값: 내용이 있는지 여부 (툴바 버튼 활성화 등에 활용)
  get hasContent(): boolean {
    const children = this.docAST?.root?.children;
    if (!children || children.length === 0) return false;
    // 루트에 단락 하나만 있고 텍스트가 없으면 빈 상태로 판단
    return !(children.length === 1 && (children[0] as any).children?.length === 0);
  }
}

export const editorStore = new EditorStore();
```

---

## 3. EditorState → MobX 연결 플러그인

📄 `apps/frontend/src/plugin/EditorStatePlugin.tsx`

```typescript
import { useEffect } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { editorStore } from '../store/editorStore';
import type { SerializedEditorState } from 'lexical';

// 에디터 업데이트마다 AST를 MobX 스토어에 동기화
export default function EditorStatePlugin() {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    return editor.registerUpdateListener(({ editorState }) => {
      editorStore.setAST(editorState.toJSON() as SerializedEditorState);
    });
  }, [editor]);

  return null;
}
```

---

## 4. 인쇄 플러그인

📄 `apps/frontend/src/plugin/PrintPlugin.tsx`

```typescript
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { $generateHtmlFromNodes } from '@lexical/html';
import printJS from 'print-js';

export function usePrint() {
  const [editor] = useLexicalComposerContext();

  const handlePrint = () => {
    editor.getEditorState().read(() => {
      const html = $generateHtmlFromNodes(editor);

      // 임시 컨테이너 생성 후 print-js에 전달 (iframe 방식)
      const containerId = '__lexical_print_target__';
      let container = document.getElementById(containerId);

      if (!container) {
        container = document.createElement('div');
        container.id = containerId;
        container.style.display = 'none';
        document.body.appendChild(container);
      }

      container.innerHTML = html;

      printJS({
        printable: containerId,
        type: 'html',
        scanStyles: true,           // 현재 페이지 스타일시트 스캔
        css: '/print.css',          // 인쇄 전용 스타일 (없으면 제거)
        onPrintDialogClose: () => {
          container!.innerHTML = '';
        },
      });
    });
  };

  return { handlePrint };
}
```

---

## 5. 툴바 컴포넌트

📄 `apps/frontend/src/component/Toolbar.tsx`

```tsx
import { observer } from 'mobx-react-lite';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { INSERT_TABLE_COMMAND } from '@lexical/table';
import { editorStore } from '../store/editorStore';
import { usePrint } from '../plugin/PrintPlugin';
import { Table, Printer } from 'lucide-react'; // lucide-react 이미 설치됨

const Toolbar = observer(() => {
  const [editor] = useLexicalComposerContext();
  const { handlePrint } = usePrint();

  const insertTable = () => {
    editor.dispatchCommand(INSERT_TABLE_COMMAND, {
      rows: '3',
      columns: '3',
    });
  };

  return (
    <div className="toolbar">
      {/* 테이블 삽입 */}
      <button onClick={insertTable} title="테이블 삽입">
        <Table size={16} />
      </button>

      {/* 인쇄 — 내용이 있을 때만 활성화 */}
      <button
        onClick={handlePrint}
        disabled={!editorStore.hasContent}
        title="인쇄"
      >
        <Printer size={16} />
      </button>
    </div>
  );
});

export default Toolbar;
```

---

## 6. Editor.tsx 수정 (핵심)

📄 `apps/frontend/src/component/Editor.tsx`

```tsx
import { LexicalComposer } from '@lexical/react/LexicalComposer';
import { ContentEditable } from '@lexical/react/LexicalContentEditable';
import { LexicalErrorBoundary } from '@lexical/react/LexicalErrorBoundary';
import { RichTextPlugin } from '@lexical/react/LexicalRichTextPlugin';
import { HistoryPlugin } from '@lexical/react/LexicalHistoryPlugin';
import { TablePlugin } from '@lexical/react/LexicalTablePlugin';
import { MarkdownShortcutPlugin } from '@lexical/react/LexicalMarkdownShortcutPlugin';
import { TRANSFORMERS } from '@lexical/markdown';

// 노드 import — 사용할 노드는 반드시 등록 필요
import { HeadingNode, QuoteNode } from '@lexical/rich-text';
import { ListNode, ListItemNode } from '@lexical/list';
import { CodeNode, CodeHighlightNode } from '@lexical/code';
import { TableNode, TableCellNode, TableRowNode } from '@lexical/table';

import EditorStatePlugin from '../plugin/EditorStatePlugin';
import Toolbar from './Toolbar';

export default function Editor() {
  return (
    <LexicalComposer
      initialConfig={{
        namespace: 'ArchitectEditor',
        onError: (e) => console.error(e),
        nodes: [
          // Markdown 변환에 필요한 노드들
          HeadingNode,
          QuoteNode,
          ListNode,
          ListItemNode,
          CodeNode,
          CodeHighlightNode,
          // 테이블 노드 (3개 세트로 등록)
          TableNode,
          TableCellNode,
          TableRowNode,
        ],
      }}
    >
      {/* 툴바는 LexicalComposer 내부에 있어야 editor context 접근 가능 */}
      <Toolbar />

      <div className="editor-shell">
        <RichTextPlugin
          contentEditable={<ContentEditable className="content-editable" />}
          placeholder={
            <div
              style={{
                position: 'absolute',
                top: '1rem',
                left: '1rem',
                opacity: 0.5,
              }}
            >
              내용을 입력하세요...
            </div>
          }
          ErrorBoundary={LexicalErrorBoundary}
        />

        {/* 플러그인 목록 */}
        <HistoryPlugin />                                    {/* Ctrl+Z 실행취소 */}
        <TablePlugin />                                      {/* 테이블 기능 활성화 */}
        <MarkdownShortcutPlugin transformers={TRANSFORMERS} />{/* ## → H2, **bold** 등 */}
        <EditorStatePlugin />                               {/* AST → MobX 동기화 */}
      </div>
    </LexicalComposer>
  );
}
```

---

## 7. 인쇄 전용 CSS (선택)

📄 `apps/frontend/public/print.css`

```css
/* 인쇄 시 에디터 UI 요소 제거 */
.toolbar {
  display: none !important;
}

/* 본문 여백 및 폰트 정리 */
body {
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 12pt;
  color: #000;
}

table {
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #000;
  padding: 6px 10px;
}
```

---

## 8. 실행 확인

```bash
# 의존성 재설치 (새 패키지 반영)
pnpm install

# 개발 서버 실행
pnpm dev
```

### 동작 확인 체크리스트

- [ ] `## ` 입력 후 스페이스 → H2로 변환
- [ ] `**텍스트**` 입력 → Bold로 변환
- [ ] `- ` 입력 → 리스트로 변환
- [ ] 툴바 테이블 버튼 → 3x3 테이블 삽입
- [ ] 인쇄 버튼 → 브라우저 인쇄 다이얼로그 (에디터 영역만)
- [ ] `Ctrl+Z` → 실행취소 동작

---

## ⚠️ 주의사항

**Toolbar는 반드시 LexicalComposer 내부에 위치해야 합니다.**
`useLexicalComposerContext()`가 Composer의 Context를 사용하기 때문에
외부에 두면 런타임 에러가 발생합니다.

**TableNode는 3개 세트로 등록해야 합니다.**
`TableNode`, `TableCellNode`, `TableRowNode` 중 하나라도 빠지면
테이블 삽입 시 에러가 발생합니다.
