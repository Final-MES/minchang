# 프로젝트 HIM-MES

## 1. 프로젝트 개요 📌

### 1.1 프로젝트 이름 📁

스마트 팩토리 MES(Manufacturing Execution System) 프로젝트

### 1.2 프로젝트 설명 📝

모듈형 MES 공정 데이터 파이프라인 설계 프로젝트입니다.

데이터 분석이 아닌, 데이터 기반 의사 결정 인프라를 구축하는 데 중점을 두었습니다.

## 📌 Why This Project?

#### 💡 선택 배경

현재 제조 산업은 단순한 자동화를 넘어, 데이터 기반 의사결정 체계로의 전환이 요구되고 있습니다.

하지만 기존의 MES 시스템은 고정된 구조와 일괄적인 기능 중심으로 설계되어 있어, 기업마다 다른 생산 환경과 요구사항을 반영하기 어렵습니다.

이에 따라 저희 팀은 기능 단위로 나눠 쉽게 조립하고 확장할 수 있는 모듈화 구조를 채택함으로써, 기업의 공정 규모나 운영 방식에 따라 유연하게 커스터마이징이 가능한 MES 플랫폼을 설계하고자 했습니다.

또한, 이 플랫폼에 MLOps를 접목하여 공정 데이터를 기반으로 한 자동 분석 및 예측 기능까지 더한, 지속적으로 진화 가능한 차세대 스마트팩토리 솔루션을 구현해보기로 했습니다.

#### 📈 시장성

중소/중견 제조업체의 스마트팩토리 도입 수요 증가

예지보전, 품질 추적, 생산 최적화 등 AI 융합 기능의 상용화 가능성

범용 MES 시장에서 모듈형 솔루션이 주목받고 있음

→ 우리 프로젝트는 커스터마이징 가능한 구조를 통해 이 수요에 대응 가능

#### ⚙️ 기술적 도전

MLOps 자동화, 실시간 공정 데이터 연동, GUI 기반 MES 구현까지

풀 스택 레벨의 통합 시스템 설계를 시도하는 것이 핵심

단순한 코드 구현을 넘어서, 현장 중심의 데이터 흐름을 체계화하는 아키텍처 설계를 목표로 함

🔧 고객 맞춤형 모듈 조립이 가능한 MES 프로그램으로, 주요 기능은 아래와 같습니다.

#### 📊 데이터 관리

실시간 기기 데이터

기계/설비 가동시간

데이터 매칭

이상 탐지

#### ✅ 품질 관리

품질 편차 측정

예지 보전

공정 분석

SPC

2. 역할 분담 🧭

이름 👤

역할 💼

주요 업무 🛠

지평진

팀장

총괄, MLOps, PPT 초안 제작, 발표

고찬국

팀원

MES 대시보드 구성

김사무엘

팀원

PPT 제작, MES GUI 구성(MFC)

송창우

팀원

MLOps

김민창

팀원 (나)

DB 설계, API 개발, 대시보드 연동, 시각화 구현

## 3. 나의 기여 ✍ (김민창)

📌 역할: 백엔드 · 데이터베이스 · 대시보드 데이터 연동 담당

MySQL 기반 데이터베이스 스키마 설계 및 RDS 구성

FastAPI 기반 진동 수집 및 고장 진단 API 서버 구축

AWS EC2 서버 운영 (Docker 포함)

Streamlit 기반 진동 데이터 시각화 구현

Next.js 대시보드와의 데이터 연동을 위한 API 구성

다중 삽입/업데이트/조회 SQL 최적화

150만 건 이상의 진동 데이터 업로드 자동화 스크립트 제작

## 🧰 기술 스택 (Used Tech Stack)

### 🔙 백엔드 / 서버
![Python](https://img.shields.io/badge/language-Python-3776AB)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-FF6F00)

### 🧮 데이터베이스
![MySQL](https://img.shields.io/badge/DB-MySQL-4479A1)
![AWS RDS](https://img.shields.io/badge/database-AWS%20RDS-527FFF)

### 🎨 대시보드 / 프론트엔드
![Streamlit](https://img.shields.io/badge/visualization-Streamlit-FF4B4B)
![Next.js](https://img.shields.io/badge/frontend-Next.js-000000)

### ☁️ 클라우드 / 배포
![AWS EC2](https://img.shields.io/badge/cloud-AWS%20EC2-FF9900)
![Docker](https://img.shields.io/badge/container-Docker-2496ED)
![Vercel](https://img.shields.io/badge/deploy-Vercel-000000)

### 🔧 개발 도구
![Git](https://img.shields.io/badge/version--control-Git-F05032)
![GitHub](https://img.shields.io/badge/repo-GitHub-181717)

### 📄 기타 정보
![version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![license](https://img.shields.io/badge/license-MIT-yellow)