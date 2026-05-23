# 🔥 Vercel 배포 트러블슈팅 기록

> 모노레포 첫 배포 시 겪은 문제와 해결 과정

---

## 문제 1 — 404 (빌드 자체가 안 됨)

### 증상
```
Build Completed in /vercel/output [11ms]
Skipping cache upload because no files were prepared
```

### 원인
`vercel.json`에 `builds` 배열이 있으면 Vercel이 자체 빌드 시스템으로만 처리하고
`buildCommand`를 완전히 무시함.

```json
// ❌ 문제 설정
{
  "builds": [...],          // 이게 있으면
  "buildCommand": "..."     // 이게 무시됨
}
```

### 해결
`builds` 배열 제거, `buildCommand`만 사용.

```json
// ✅ 수정 후
{
  "version": 2,
  "buildCommand": "pnpm turbo run build",
  "installCommand": "pnpm install"
}
```

---

## 문제 2 — 500 (ESM 인식 실패)

### 증상
```
SyntaxError: Cannot use import statement outside a module
Failed to load the ES module: /var/task/server.js.
Make sure to set "type": "module" in the nearest package.json file
```

### 원인
Rollup이 `format: 'es'`로 ESM 번들을 생성하는데,
Vercel Serverless 환경의 `/var/task/`에는 `package.json`이 없어서
Node.js가 CJS로 로드 시도함.

### 해결
Rollup 빌드 후 `dist/package.json`을 자동 생성하는 플러그인 추가.

```js
// rollup.config.js
import { writeFileSync } from 'fs';

const emitPackageJson = () => ({
  name: 'emit-package-json',
  writeBundle() {
    writeFileSync(
      'dist/package.json',
      JSON.stringify({ type: 'module' }, null, 2)
    );
  },
});
```

그리고 `vercel.json`의 `includeFiles`에 `dist/**` 추가해서
`dist/package.json`이 배포에 포함되도록 설정.

```json
"functions": {
  "apps/backend/dist/server.js": {
    "includeFiles": "apps/backend/dist/**,apps/backend/public/**"
  }
}
```

---

## 문제 3 — 파일명 불일치 (Turbo 캐시 문제)

### 증상
```
// 빌드 로그
@summary/frontend:build: cache hit, replaying logs
../backend/public/assets/index-CJkbqb-1.js  ← 빌드된 파일명

// 브라우저 요청
GET /assets/index-DavzgfoG.js → 404  ← 이전 배포 파일명 요청
```

### 원인
Turbo Remote Cache 히트 시 **로그만 재생**하고 실제 파일을 디스크에 쓰지 않음.
`turbo.json`의 `outputs`가 `dist/**`만 잡고 있어서
프론트엔드 결과물이 가는 `backend/public/`이 캐시 복원 대상에서 빠짐.

```json
// ❌ 문제 설정
"outputs": ["dist/**"]   // public/** 누락
```

### 해결
`turbo.json` outputs에 `public/**` 추가.

```json
// ✅ 수정 후
"outputs": ["dist/**", "public/**"]
```

이후 Turbo 캐시 강제 무효화를 위해 Vercel 환경변수 일시 추가.

```
VERCEL_FORCE_NO_BUILD_CACHE = 1
```

새 캐시가 `public/**`까지 포함해서 잡힌 후 환경변수 제거.

### 확인 방법
빌드 로그에서 아래 두 가지 확인:

```
// 캐시 강제 무효화 시
cache bypass, force executing   ← 실제 빌드 실행됨
Cached: 0 cached, 2 total       ← 캐시 미사용 확인

// 이후 정상 캐시 히트 시
cache hit, replaying logs
public/assets/index-XXX.js      ← 파일이 실제로 복원되어야 함
```

---

## 교훈 정리

| 문제 | 핵심 원인 | 해결 키워드 |
|---|---|---|
| 빌드 안 됨 | `builds` + `buildCommand` 충돌 | `builds` 제거 |
| ESM 인식 실패 | `/var/task/`에 `package.json` 없음 | `dist/package.json` 주입 |
| 파일명 불일치 | Turbo outputs 누락 | `public/**` 추가 |
