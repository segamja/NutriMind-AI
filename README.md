# NutriMind AI

**Snap. Analyze. Improve.**

사진 한 장으로 음식과 영양소를 분석하고, AI가 건강 상태를 분석하여 맞춤형 식단과 건강 코칭을 제공하는 AI Nutrition Coach 플랫폼입니다.

## 기술 스택

| Layer | Stack |
|-------|-------|
| Frontend | React 18+, TypeScript, Vite, TailwindCSS, Zustand |
| Backend | FastAPI, Python |
| AI | OpenAI Vision API, Chat Completions (Structured JSON) |
| Database | SQLite (MVP) |

## Phase 1 MVP 기능

- 음식 촬영 / 업로드
- CNN 음식 인식 (Mock — 추후 EfficientNet-B3 연동)
- OpenAI Vision 분석 (재료, 양, 영양소, 건강 점수)
- AI 코칭 (OpenAI Responses)
- 식사 기록 저장
- Health Dashboard
- 다크모드 지원

## 배포 (Vercel + Supabase)

인터넷에서 실행하려면 [docs/DEPLOY.md](docs/DEPLOY.md)를 참고하세요.

| 서비스 | 역할 |
|--------|------|
| **Vercel** | Frontend + Backend API |
| **Supabase** | PostgreSQL Database |

```bash
# GitHub push → Vercel 자동 배포
# 환경변수: OPENAI_API_KEY, DATABASE_URL (Supabase), CORS_ORIGINS
```

---

## 시작하기 (로컬)

### 1. Backend 설정

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 설정

uvicorn main:app --reload --port 8800
```

### 2. Frontend 설정

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 http://localhost:5173 접속

### 3. OpenAI API Key

`backend/.env` 파일에 API 키를 설정하세요:

```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

## API 엔드포인트

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | 서버 상태 확인 |
| POST | `/api/scan` | 음식 이미지 분석 |
| POST | `/api/meals` | 식사 기록 저장 |
| GET | `/api/meals` | 식사 기록 조회 |
| GET | `/api/meals/today` | 오늘 식사 조회 |
| POST | `/api/coach` | AI 코칭 채팅 |
| GET | `/api/dashboard/stats` | 대시보드 통계 |

## 프로젝트 구조

```
NutriMind-AI/
├── backend/
│   ├── main.py
│   ├── app/
│   │   ├── config.py
│   │   ├── models/schemas.py
│   │   ├── services/
│   │   │   ├── cnn_service.py      # CNN Mock
│   │   │   └── openai_service.py   # Vision + Coach
│   │   ├── routers/
│   │   └── db/database.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/          # Home, Camera, Result, Dashboard, History, Coach
│       ├── components/     # UI Components
│       ├── store/          # Zustand State
│       └── lib/            # API Client
└── docs/
    └── TECH_SPEC.md
```

## 개발 원칙

- OpenAI API는 Backend에서만 호출
- API Key는 환경변수 관리
- 모든 AI 응답은 Structured JSON
- 모바일 우선 UI, 다크모드 지원
- Card 기반 UI 컴포넌트

## 라이선스

MIT
