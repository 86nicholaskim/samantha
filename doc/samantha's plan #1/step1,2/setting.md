# 🚀 Node.js + TS 프로젝트 로컬 구축 가이드

이 가이드는 Turbo + Rollup 환경을 기반으로 하며, 각 블록의 내용을 해당 파일명으로 저장하시면 됩니다.

## 1. 초기화 및 패키지 설치터미널에서 아래 명령어를 순서대로 실행하세요.

```bash
# 프로젝트 생성 및 이동
# 1. 프로젝트 폴더 생성 및 이동
mkdir my-app && cd my-app

# 2. pnpm 초기화 (package.json 생성)
pnpm init

# 3. 운영 의존성 설치 (Express, Dotenv)
pnpm add express dotenv

# 4. 개발 의존성 설치 (TS, 빌드툴, 린트)
pnpm add -D typescript @types/node @types/express tslib rollup @rollup/plugin-typescript @rollup/plugin-node-resolve turbo nodemon eslint prettier eslint-config-prettier eslint-plugin-prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin


```

## 2. 기본 설정 파일 (Root 폴더)

📄 package.json
프로젝트의 실행 스크립트와 모듈 방식을 정의합니다.

```json
{
  "name": "my-node-app",
  "version": "1.0.0",
  "type": "module", // ESM(import/export) 사용을 위한 필수 설정
  "scripts": {
    "dev": "turbo run dev", // 개발 서버 실행 (타입체크 + 빌드감시)
    "build": "turbo run build", // 운영용 빌드 실행
    "type-check": "tsc --noEmit", // 파일 생성 없이 타입 에러만 체크
    "lint": "eslint 'src/**/*.ts'", // 코드 문법 검사
    "format": "prettier --write 'src/**/*.ts'" // 코드 스타일 자동 교정
  }
}
```

📄 tsconfig.json
TypeScript 컴파일 규칙입니다. 번들러(Rollup) 환경에 최적화되어 있습니다.

```json
{
  "compilerOptions": {
    "target": "ESNext", // 최신 자바스크립트로 변환
    "module": "ESNext", // 최신 모듈 시스템 사용
    "moduleResolution": "Bundler", // Rollup 같은 번들러에 최적화된 해석 방식
    "rootDir": "./src", // 소스 위치
    "outDir": "./dist", // 빌드 결과물 위치
    "strict": true, // 엄격한 타입 체크 활성화
    "noEmit": true, // tsc는 타입 체크만 수행 (빌드는 Rollup이 담당)
    "esModuleInterop": true, // CJS 모듈 호출 호환성 허용
    "skipLibCheck": true, // 라이브러리 타입 체크 건너뛰기
    "verbatimModuleSyntax": true, // import 구문 최적화 유지
    "isolatedModules": true, // 각 파일을 독립 모듈로 처리 (번들러 필수)
    "types": ["node"] // Node.js 환경 타입 로드
  },
  "include": ["src/**/*"] // 검사 대상 범위
}
```

📄 rollup.config.js
소스 코드를 하나로 묶고 최적화하는 빌드 공정 설정입니다.

```javascript
import typescript from '@rollup/plugin-typescript';
import resolve from '@rollup/plugin-node-resolve';

export default {
  input: 'src/app.ts', // 빌드 시작점
  output: {
    dir: 'dist', // 결과물 저장 폴더
    format: 'es', // ESM 형식으로 출력
    sourcemap: true, // 디버깅용 소스맵 생성
    entryFileNames: '[name].js',
  },
  plugins: [
    resolve(), // node_modules 패키지 해석
    typescript({
      tsconfig: './tsconfig.json',
      noEmit: false, // 빌드 시에는 파일을 생성해야 하므로 오버라이드
    }),
  ],
  external: ['express', 'dotenv'], // 외부 라이브러리는 번들에서 제외
};
```

📄 turbo.json
빌드 자동화 및 캐싱 시스템 설정입니다.

```json
{
  "$schema": "https://turbo.build",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"] // 빌드 결과물을 캐싱하여 다음 빌드 속도 향상
    },
    "dev": {
      "cache": false, // 개발 모드는 캐싱하지 않음
      "persistent": true // 프로세스 상주 설정
    }
  }
}
```

## 3. 에디터 및 환경 설정

📄 .gitignore

```text
node_modules/
dist/
.env
.turbo/

```

📄 .vscode/settings.json (폴더 없으면 생성)
저장 시 자동으로 코드를 정돈하도록 VSCode를 설정합니다.

```json
{
  "editor.formatOnSave": true, // 저장 시 자동 포맷팅
  "editor.defaultFormatter": "esbenp.prettier-vscode", // 기본 포맷터를 Prettier로
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit" // 저장 시 ESLint 에러 자동 수정
  }
}
```

## 4. 소스 코드 작성 및 실행

📄 src/app.ts (폴더 생성 필요)

```typescript
import express, { Request, Response } from 'express';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req: Request, res: Response) => {
  res.json({ status: 'success', message: 'Build Pipeline Ready!' });
});

app.listen(PORT, () => {
  console.log(`🚀 Server is running at http://localhost:${PORT}`);
});
```

📄 .env

```text
PORT=3000

```

## 5. 실행 명령어 요약

- 의존성 설치: pnpm install
- 개발 시작: pnpm dev (코드 수정 시 실시간 반영)
- 최종 빌드: pnpm build (운영 서버 배포용 파일 생성)
- 품질 검사: pnpm type-check 및 pnpm lint
