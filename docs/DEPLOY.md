# NutriMind AI — Vercel + Supabase 배포 가이드

인터넷에서 NutriMind AI를 실행하려면 **Vercel**(Frontend + API)과 **Supabase**(PostgreSQL DB)를 설정합니다.

GitHub에 코드만 올려서는 실행되지 않습니다. 아래 순서대로 진행하세요.

---

## 아키텍처

```
사용자 브라우저
    ↓
Vercel (React UI + FastAPI /api/*)
    ↓                    ↓
OpenAI API          Supabase PostgreSQL
```

---

## 1단계: Supabase 설정

### 1-1. 프로젝트 생성

1. [supabase.com](https://supabase.com) 가입
2. **New Project** → 이름: `nutrimind-ai`
3. Database Password 저장 (나중에 필요)

### 1-2. 테이블 생성

1. Supabase Dashboard → **SQL Editor**
2. [`supabase/schema.sql`](../supabase/schema.sql) 내용 붙여넣기 → **Run**

### 1-3. Connection String 복사

1. **Project Settings** → **Database**
2. **Connection string** → **URI** 탭
3. **Transaction pooler** (포트 6543) 선택
4. `[YOUR-PASSWORD]`를 실제 비밀번호로 교체

예시:
```
postgresql://postgres.xxxxx:YOUR_PASSWORD@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres
```

---

## 2단계: Vercel 배포

### 2-1. GitHub 연동

1. [vercel.com](https://vercel.com) 가입 (GitHub 연동)
2. **Add New Project** → `segamja/NutriMind-AI` Import
3. Framework Preset: **Other** (자동 감지됨)

### 2-2. Build 설정 (기본값 확인)

| 설정 | 값 |
|------|-----|
| Root Directory | `.` (프로젝트 루트) |
| Build Command | `cd frontend && npm run build` |
| Output Directory | `frontend/dist` |
| Install Command | `cd frontend && npm install` (**pip install 사용 금지**) |

> `vercel.json`이 이미 포함되어 있어 대부분 자동 적용됩니다.

### 2-3. Environment Variables (필수)

Vercel Project → **Settings** → **Environment Variables**:

| Key | Value | 설명 |
|-----|-------|------|
| `OPENAI_API_KEY` | `sk-...` | OpenAI API 키 |
| `OPENAI_MODEL` | `gpt-4o-mini` | 코칭/리포트 모델 |
| `OPENAI_VISION_MODEL` | `gpt-4o-mini` | Vision 분석 모델 |
| `DATABASE_URL` | `postgresql://...` | Supabase Connection String |
| `CORS_ORIGINS` | `https://your-app.vercel.app` | 배포 후 Vercel URL |

배포 후 실제 URL이 나오면 `CORS_ORIGINS`를 업데이트하고 **Redeploy** 하세요.

### 2-4. Deploy

**Deploy** 클릭 → 완료 후 URL 확인

예: `https://nutrimind-ai.vercel.app`

---

## 3단계: 동작 확인

1. `https://your-app.vercel.app` 접속
2. **스캔** → 음식 사진 업로드 → AI 분석
3. **식사 기록** 저장
4. **코치** → AI 상담
5. **리포트** → 주간 리포트 (식사 1건 이상 필요)

API 헬스체크:
```
https://your-app.vercel.app/api/health
```

---

## 로컬 vs 배포 차이

| 항목 | 로컬 | Vercel + Supabase |
|------|------|-------------------|
| Frontend | `npm run dev` (5173) | Vercel CDN |
| Backend | `uvicorn` (8800) | Vercel Serverless `/api/*` |
| DB | SQLite 파일 | Supabase PostgreSQL |
| API URL | `/api` (Vite proxy) | `/api` (same domain) |

로컬 개발은 기존처럼 Backend + Frontend를 각각 실행하면 됩니다.

---

## 주의사항

### Serverless 타임아웃
- Vercel **Hobby**: 함수 최대 10초
- OpenAI Vision 분석이 10초를 넘으면 **Pro** 플랜(60초) 업그레이드 필요
- `vercel.json`에 `maxDuration: 60` 설정됨 (Pro 필요)

### 이미지 업로드
- Vercel Serverless 요청 크기 제한: **4.5MB**
- 큰 사진은 업로드 전 리사이즈 권장

### API Key 보안
- `OPENAI_API_KEY`는 **Vercel Environment Variables**에만 저장
- GitHub에 `.env` 파일 커밋 금지 (`.gitignore`에 포함됨)

---

## 문제 해결

| 증상 | 해결 |
|------|------|
| API 404 | `vercel.json` rewrites 확인, Redeploy |
| DB 연결 실패 | `DATABASE_URL` 형식 확인 (Transaction pooler, 6543) |
| CORS 에러 | `CORS_ORIGINS`에 Vercel URL 추가 후 Redeploy |
| 분석 타임아웃 | Vercel Pro 업그레이드 또는 더 빠른 모델 사용 |
| 리포트 400 | 식사 기록 1건 이상 저장 후 재시도 |

---

## Supabase Storage (선택)

식사 사진을 영구 저장하려면:

1. Supabase → **Storage** → **New bucket** → `meal-images` (public)
2. Vercel env에 추가:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`

(Storage 업로드 연동은 Phase 2에서 추가 가능)

---

## 배포 후 URL 공유

배포가 완료되면 Vercel URL을 공유하면 누구나 브라우저에서 NutriMind AI를 사용할 수 있습니다.

```
https://your-app.vercel.app
```
