# 🌐 Node.js Full-Stack 관리 워크플로우 총정리

이 문서는 **TypeScript + pnpm + Turbo + Rollup** 기반의 현대적 웹 시스템의 설계, 개발, 검증, 배포 전 과정을 다룹니다.

---

## 1단계: 프로젝트 초기화 및 로컬 설정 (Setup)

프로젝트의 뼈대를 잡고 엄격한 타입 시스템과 빌드 도구를 구성합니다.

### 📦 주요 의존성 구성

- **Dependencies**: `express`, `dotenv` (실제 운영 서버 실행에 필수)
- **DevDependencies**: `typescript`, `rollup`, `turbo`, `eslint`, `prettier` 등 (개발 및 빌드 도구)

### 🛠️ 핵심 설정 파일

- **`package.json`**: `"type": "module"` 설정을 통해 ESM 환경 구축.
- **`tsconfig.json`**: `moduleResolution: "Bundler"`, `noEmit: true` 설정으로 번들러 최적화.
- **`rollup.config.js`**: `src/server.ts`를 엔트리로 최적화된 JS 번들 생성.

---

## 2단계: 레이어드 아키텍처 설계 (Development)

SaaS급 유지보수성을 위해 **설정(App)**과 **실행(Server)**을 분리합니다.

### 📄 `src/app.ts` (설정부)

- Express 인스턴스 생성 및 라우터/미들웨어 설정.
- `export default app;`을 통해 테스트 및 서버리스 환경 호환성 확보.

### 📄 `src/server.ts` (실행부)

- `NODE_ENV`를 체크하여 로컬 환경에서만 `app.listen` 실행.
- Vercel과 같은 서버리스 플랫폼을 위해 `app` 객체를 다시 `export`.

---

## 3단계: 지속적 통합 (CI: GitHub Actions)

코드 푸시 시마다 원격 서버에서 품질을 자동으로 검증하여 "빌드가 깨지는 코드"의 유입을 차단합니다.

### 📄 `.github/workflows/ci.yml` 워크플로우

1.  **Checkout**: 최신 소스 코드 로드.
2.  **pnpm Setup**: 패키지 설치 및 캐싱.
3.  **Type Check**: `pnpm type-check` (`tsc --noEmit`) 실행.
4.  **Lint**: `pnpm lint` (`eslint`) 실행.
5.  **Build**: `pnpm build` (`rollup -c`) 실행.

---

## 4단계: 지속적 배포 (CD: Vercel)

검증된 코드를 전 세계 어디서든 접속 가능한 실제 URL로 자동 배포합니다.

### 📄 `vercel.json` 설정

- `@vercel/node` 빌더를 사용하여 `src/server.ts`를 서버리스 함수로 변환.
- 모든 경로(`/(.*)`)를 서버 엔트리 포인트로 라우팅.

### ⚠️ 배포 핵심 체크리스트

- **Dependencies 확인**: `express` 등이 `devDependencies`에 있으면 500 에러 발생.
- **확장자 명시**: ESM 규칙에 따라 `import` 시 반드시 `.js` 확장자 포함.

---

## 5단계: 브랜치 보호 및 운영 (Governance)

검수 시스템을 GitHub에 적용합니다.

### 🛡️ Branch Protection Rules

- **PR 필수**: `master` 브랜치 직접 Push 차단.
- **Status Check 강제**: CI 워크플로우(`build-and-test`) 성공 시에만 Merge 가능.
- **Linear History**: 히스토리 관리를 위해 Squash/Rebase 머지 권장.

---

## 🚀 주요 명령어 요약

| 명령어            | 용도        | 설명                                  |
| :---------------- | :---------- | :------------------------------------ |
| `pnpm dev`        | 개발 모드   | Turbo 기반 실시간 코드 감시 및 실행   |
| `pnpm build`      | 로컬 빌드   | Rollup을 통한 프로덕션 번들 생성      |
| `pnpm type-check` | 타입 검사   | 전체 프로젝트의 정적 타입 오류 검사   |
| `pnpm lint`       | 코드 정돈   | ESLint 및 Prettier 규칙 위반 검사     |
| `pnpm start`      | 서비스 실행 | 빌드된 결과물(`dist/`) 기반 서버 구동 |
