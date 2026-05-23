# 🚀 Step 3: Vercel 배포 설정 가이드

> pnpm + Turbo v2 모노레포를 Vercel에 배포하는 설정

---

## 📁 구조 개요

```
summary/                        ← Vercel Root Directory
├── vercel.json                 ← Vercel 배포 설정
├── turbo.json                  ← Turbo 빌드 파이프라인
└── apps/
    ├── frontend/               ← Vite 빌드 → backend/public/ 주입
    └── backend/                ← Express 서버, public/ 정적 서빙
        └── public/             ← 프론트엔드 빌드 결과물
```

---

## 🔄 빌드 흐름

```
pnpm turbo run build
    ↓
1. @summary/frontend:build  (Vite)
   → apps/backend/public/ 에 결과물 주입
    ↓
2. @summary/backend:build   (Rollup)
   → apps/backend/dist/server.js 생성
    ↓
Vercel이 dist/server.js를 Serverless Function으로 서빙
Express가 public/ 정적 파일 서빙
```

---

## ⚙️ 설정 파일

### vercel.json (루트)

```json
{
  "version": 2,
  "buildCommand": "pnpm turbo run build",
  "installCommand": "pnpm install",
  "routes": [
    {
      "src": "/(.*)",
      "dest": "apps/backend/dist/server.js"
    }
  ],
  "functions": {
    "apps/backend/dist/server.js": {
      "includeFiles": "apps/backend/dist/**,apps/backend/public/**"
    }
  }
}
```

**핵심 포인트**
- `builds` 배열 사용 시 `buildCommand`가 무시됨 → `builds` 제거
- `includeFiles`에 `dist/**` + `public/**` 모두 포함해야 함
- `dist/package.json` (`type: module`)이 포함되어야 ESM 인식

### turbo.json (루트)

```json
{
  "$schema": "https://turbo.build",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "public/**"]
    },
    "type-check": { "cache": true },
    "lint": { "cache": true },
    "dev": { "cache": false, "persistent": true }
  }
}
```

**핵심 포인트**
- `outputs`에 `public/**` 추가 필수
- 없으면 Turbo 캐시 히트 시 `public/` 파일이 복원되지 않음
- `"dependsOn": ["^build"]` → frontend가 먼저 빌드되고 backend가 나중에 빌드되는 순서 보장

### rollup.config.js (apps/backend/)

```js
// dist/package.json 생성 플러그인 — ESM 인식을 위해 필요
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

Vercel Serverless 환경에서 `dist/server.js`가 ESM임을 인식시키기 위해
`dist/package.json`에 `{ "type": "module" }`을 주입해야 함.

---

## 🖥️ Vercel Dashboard 설정

| 항목 | 값 |
|---|---|
| Root Directory | `/` (기본값) |
| Build Command | vercel.json이 처리 (Override 불필요) |
| Output Directory | vercel.json이 처리 (Override 불필요) |
| Install Command | `pnpm install` |

---

## ✅ 배포 확인 체크리스트

- [ ] `vercel.json`에 `builds` 배열 없음
- [ ] `turbo.json` outputs에 `public/**` 포함
- [ ] `rollup.config.js`에 `emitPackageJson` 플러그인 포함
- [ ] `dist/package.json` 생성 확인 (`{ "type": "module" }`)
- [ ] Vercel 빌드 로그에서 `Tasks: 2 successful` 확인
- [ ] 배포 후 사이트 정상 접속 확인
