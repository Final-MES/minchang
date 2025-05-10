# 프로젝트 HIM-MES

## 1. 프로젝트 개요 📌

### 1.1 프로젝트 이름 📁

스마트 팩토리 MES(Manufacturing Execution System) 프로젝트

### 1.2 프로젝트 설명 📝

모듈형 MES 공정 데이터 파이프라인 설계 프로젝트입니다.

데이터 분석이 아닌, 데이터 기반 의사 결정 인프라를 구축하는 데 중점을 두었습니다.

## 참여자
- 김민창 (DB/백엔드/대시보드)
- 지평진, 고찬국, 김사무엘, 송창우

---

## 1. 내가 맡은 역할 ✍

### ☁️ 클라우드 서버 관리
- AWS EC2 인스턴스를 이용한 FastAPI 서버 호스팅
- Docker를 이용한 FastAPI 컨테이너화 및 배포 자동화
- AWS RDS(MySQL) 연동 및 보안 그룹, 포트 관리

### 🗄️ DB 설계 및 관리
- MySQL 기반 진동 수집 및 진단 테이블 스키마 설계
- SQLAlchemy를 이용한 ORM 매핑 및 데이터 모델링
- 측정시간 기반 대용량 데이터 저장 및 조회 쿼리 최적화
- 150만 건 이상 진동 데이터를 중복 검사 및 자동 업로드 스크립트 구현

### 🔧 API 개발 및 관리
- FastAPI 기반 RESTful API 설계 및 구현
- `/vibration-data`, `/vibration-diagnosis` 등 진동 수집 및 진단 데이터 관리 API 개발
- 기계별 최근 진단 데이터 조회를 위한 고급 SQL 서브쿼리 및 응답 구조 설계
- Swagger 문서 자동화 및 팀원 테스트 환경 제공

### 🎨 대시보드 제작
- Streamlit 기반 진동 파형 시각화 대시보드 개발
- Vercel에 배포된 Next.js 기반 진단 결과 시계열 그래프 페이지 제작
- Recharts, Chart.js 등 라이브러리 활용하여 실시간 고장 히스토리 시각화
- 사용자 선택 필터(기계명, 날짜, 상태 유형) 및 커스텀 툴팁 UI 구성

## 2. 🧰 사용 기술 스택 (Used Tech Stack)

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