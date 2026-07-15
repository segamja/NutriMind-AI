# NutriMind AI 기술명세서 (Technical Specification)

Version: 1.0

---

# 1. 프로젝트 개요

## 프로젝트명

NutriMind AI

## 슬로건

**Snap. Analyze. Improve.**

사진 한 장으로 음식과 영양소를 분석하고, AI가 건강 상태를 분석하여 맞춤형 식단과 건강 코칭을 제공하는 AI Nutrition Coach 플랫폼이다.

본 프로젝트는 CalAI를 벤치마킹하지만 단순한 칼로리 계산 앱이 아닌 AI 건강 코치 서비스를 목표로 한다.

---

# 2. 프로젝트 목표

NutriMind AI는 다음 기능을 제공한다.

- 음식 사진 자동 인식
- 음식 재료 분석
- 음식 양(Portion) 추정
- 칼로리 계산
- 영양소 분석
- 건강 점수 계산
- AI 식단 코칭
- 장기 식습관 분석
- 질병 위험도 예측
- 건강 리포트 자동 생성
- AI 식단 생성
- AI 음식 이미지 생성

AI가 단순히 결과만 보여주는 것이 아니라 사용자가 다음에 무엇을 해야 하는지(Action)를 제안하는 것이 핵심이다.

---

# 3. 핵심 차별화

기존 서비스

사진

↓

음식 인식

↓

칼로리 제공

NutriMind AI

사진

↓

CNN 음식 인식

↓

OpenAI Vision 분석

↓

영양소 계산

↓

데이터 분석

↓

건강 점수 계산

↓

AI 코칭

↓

다음 식사 추천

↓

AI 이미지 생성

---

# 4. 주요 기능

## 4.1 AI Food Scanner

사용자가 음식 사진을 촬영하면

- 음식 종류 인식
- 재료 분석
- 음식 양 추정
- 영양소 계산

을 자동 수행한다.

---

## 4.2 CNN 음식 인식

딥러닝 CNN 모델을 이용하여 음식을 분류한다.

추천 모델

- EfficientNet-B3
- MobileNetV3

추천 데이터셋

- Food101
- UECFood256
- 한국 음식 데이터셋

CNN은 음식 종류를 분류하는 역할을 담당한다.

---

## 4.3 YOLO 음식 검출

YOLO를 이용하여

- 음식 위치
- 여러 음식 동시 검출

을 수행한다.

예)

비빔밥

김치

계란

국

반찬

각각을 개별 검출한다.

---

## 4.4 OpenAI Vision 분석

OpenAI Vision API를 이용하여

- 재료 분석
- 조리 방식 추론
- 음식 설명
- 음식 양 보정

을 수행한다.

예)

비빔밥

↓

소고기

계란

당근

시금치

고추장

콩나물

---

## 4.5 Portion Estimation

사진을 기반으로

음식의 양을 추정한다.

예)

밥 180g

계란 55g

소고기 80g

---

## 4.6 Nutrition Analysis

자동 계산

- Calories
- Protein
- Fat
- Carbohydrates
- Fiber
- Sugar
- Sodium
- Calcium
- Iron
- Potassium

---

## 4.7 AI Nutrition Coach

OpenAI Responses API를 이용하여

사용자의 식습관을 분석한다.

예시

"오늘은 단백질 섭취가 부족합니다."

"나트륨 섭취량이 권장량보다 높습니다."

"저녁에는 단백질 위주의 식사를 추천합니다."

---

## 4.8 Meal Score

AI가 식사를 평가한다.

평가 항목

- 칼로리
- 단백질
- 지방
- 탄수화물
- 당류
- 나트륨
- 식이섬유

최종

Health Score

0~100점

---

## 4.9 Health Dashboard

사용자에게

- 일간
- 주간
- 월간

통계를 제공한다.

그래프

- 칼로리
- 단백질
- 지방
- 체중
- BMI
- 운동량
- 물 섭취량

---

## 4.10 AI Meal Planner

사용자의 목표

- 다이어트
- 근육 증가
- 유지
- 저탄고지
- 당뇨식

에 맞는 식단을 생성한다.

---

## 4.11 AI Refrigerator

냉장고 사진을 촬영하면

AI가

재료를 인식하여

추천 요리를 생성한다.

---

## 4.12 Healthy Alternative

건강하지 않은 음식을

더 건강한 음식으로 변경해준다.

예)

햄버거

↓

통밀버거

↓

샐러드

↓

제로콜라

---

## 4.13 Disease Risk Prediction

사용자의

- BMI
- 체중
- 식습관
- 운동량
- 영양 섭취

데이터를 이용하여

생활습관 기반 위험도를 예측한다.

예)

당뇨

고혈압

비만

심혈관질환

※ 의료 진단이 아닌 참고 정보 제공

---

## 4.14 Weekly AI Report

매주

OpenAI가 자동으로

건강 리포트를 생성한다.

포함 내용

- 식습관 분석
- 영양소 분석
- 건강 점수
- 개선사항
- 다음 주 목표

---

## 4.15 AI Nutrition Chat

사용자는 자유롭게 질문할 수 있다.

예)

오늘 치킨 먹어도 될까?

단백질이 부족한가?

오늘 저녁 추천해줘

냉장고 재료로 만들 수 있는 음식은?

---

# 5. AI Pipeline

Camera

↓

YOLO Object Detection

↓

CNN Food Classification

↓

OpenAI Vision

↓

Nutrition Database

↓

Health Analytics

↓

OpenAI Responses API

↓

AI Coach

---

# 6. OpenAI 활용

## Vision API

- 음식 분석
- 재료 분석
- 조리법 추론

## Responses API

- 영양 코칭
- 식단 추천
- 건강 상담
- 건강 리포트

## Image Generation API

- 추천 식단 이미지
- 레시피 이미지
- 건강한 대체 음식 생성

## Structured Output

모든 AI 응답은 JSON으로 반환한다.

---

# 7. 데이터 분석

Python 기반 데이터 분석

사용 라이브러리

- Pandas
- NumPy
- Scikit-Learn

분석 내용

- 식습관 패턴
- 칼로리 추이
- 체중 변화
- BMI 변화
- 단백질 부족
- 나트륨 과다
- 식단 균형

---

# 8. 시스템 아키텍처

Frontend

React + TypeScript + Vite

↓

Backend

FastAPI

↓

CNN Engine

PyTorch

↓

YOLO

↓

OpenAI API

↓

PostgreSQL

↓

Supabase Storage

---

# 9. 기술 스택

Frontend

- React 18
- TypeScript
- Vite
- TailwindCSS
- shadcn/ui
- Zustand

Backend

- FastAPI
- Python

AI

- OpenAI Responses API
- OpenAI Vision API
- OpenAI Image Generation API

Deep Learning

- PyTorch
- TorchVision
- EfficientNet-B3
- MobileNetV3
- YOLOv11

Database

- PostgreSQL

Storage

- Supabase Storage

Deployment

- Vercel
- Railway
- Supabase

---

# 10. UI 구성

- Home
- Camera
- Scanner Result
- Dashboard
- History
- AI Coach
- Meal Planner
- Weekly Report
- Profile
- Settings

---

# 11. 개발 원칙

- React + TypeScript 사용
- Vite 기반 프로젝트
- TailwindCSS 사용
- 컴포넌트 기반 설계
- OpenAI API는 반드시 Backend에서 호출
- API Key는 환경변수 관리
- CNN과 OpenAI Vision 역할 분리
- AI 기능은 모듈화
- 모든 분석 결과는 카드(Card) 형태 UI 제공
- 모바일 우선(Mobile First) UI 설계
- 다크모드 지원
- 로딩 애니메이션 및 에러 처리 제공

---

# 12. MVP 범위

Phase 1

- 음식 촬영
- CNN 음식 인식
- OpenAI Vision 분석
- 영양소 계산
- AI 코칭
- 식사 기록

Phase 2

- 건강 점수
- 주간 리포트
- AI 식단 추천
- 장보기 리스트
- 건강 대시보드

Phase 3

- 냉장고 분석
- 질병 위험도 예측
- AI 이미지 생성
- 가족 계정
- 웨어러블 연동

---

# 13. 최종 목표

NutriMind AI는 단순한 칼로리 계산 앱이 아니라

AI가

사용자의 식습관을 이해하고

건강을 분석하며

맞춤형 행동(Action)을 제안하는

차세대 AI Nutrition Coach 플랫폼을 목표로 한다.