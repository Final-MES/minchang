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

## 내가 했던 일들에 대한 자세한 개요.

## 1. DB (MySQL)

### ✅ 어떤 작업을 했는가?

MES 시스템의 진동 수집 및 AI 진단 결과 처리를 위한 데이터베이스를 설계하였습니다.  
초기에는 AI 학습 데이터의 구조조차 명확하지 않은 상태였고, 이에 따라 일반적인 MES 구성을 바탕으로 예비 테이블을 작성하였습니다.

---

### 🔎 초기 예비 테이블 설계

초기에는 MES에서 일반적으로 필요한 정보를 기반으로 다음과 같은 테이블을 예상하여 설계하였습니다.

```sql
-- 설비 마스터 테이블
CREATE TABLE equipment_info (
    equipment_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    installed_at DATE
);

-- 설비 상태 기록 테이블
CREATE TABLE equipment_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    equipment_id VARCHAR(50),
    image_path VARCHAR(255),
    status ENUM('running', 'stop', 'error') DEFAULT 'stop',
    temperature DECIMAL(10,3),
    speed DECIMAL(10,3),
    runtime DECIMAL(10,3),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment_info(equipment_id)
);

-- 이상 탐지 기록 테이블
CREATE TABLE anomaly_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    equipment_id VARCHAR(50),
    model_name VARCHAR(30),
    message VARCHAR(255),
    severity ENUM('1','2','3','4','5'),
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment_info(equipment_id)
);

-- 품질 검사 기록 테이블
CREATE TABLE quality_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(50),
    equipment_id VARCHAR(50),
    measure_item VARCHAR(20),
    measured_value DECIMAL(10,3),
    target_value DECIMAL(10,3),
    tolerance DECIMAL(10,3),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment_info(equipment_id)
);
```
📌 참고: 당시에는 AI 학습 데이터의 구조와 진단 결과 형식에 대한 정보가 부족하여, 일반적인 예측 보전 시스템의 구조에 맞추어 설계하였습니다.

🧩 문제 파악 및 분석
이후 MLOps 팀 및 수집 데이터 파일을 분석한 결과, 사용 데이터는 회전기계의 진동 데이터를 기반으로 하며, 일부러 고장 상태를 만들어 측정한 센서 값임을 확인했습니다.

측정 시간 (measured_time)

각 고장 유형별 진동 수치:

normal (정상 상태)

unbalance (질량 불균형)

looseness (지지 불량)

unbalance_looseness (복합 고장)

또한 AI 진단 결과는 0~3 범위의 숫자로 출력되며, 각각 다음과 같은 상태를 의미합니다:

0: 정상

1: 질량 불균형

2: 지지 불량

3: 복합 불량

📸 센서 데이터 예시
아래는 실제 사용된 회전기계 진동 데이터(g1_sensor1.csv)의 일부입니다.
![센서 데이터 예시](./images/sensor_data_example.png)

컬럼 설명:

A열: 측정 시간 (measured_time)

B~E열: 각 고장 유형에 해당하는 진동 값

🛠️ 최종 테이블 설계
위 데이터를 기반으로, 복잡도를 낮추고 목적에 집중된 다음과 같은 테이블로 재설계하였습니다.

```sql
-- 진동 수집 데이터 테이블
CREATE TABLE vibration_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_name VARCHAR(50) NOT NULL,
    sensor_no VARCHAR(20) NOT NULL,
    collected_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    measured_time FLOAT NOT NULL,
    normal FLOAT NOT NULL,
    unbalance FLOAT NOT NULL,
    looseness FLOAT NOT NULL,
    unbalance_looseness FLOAT NOT NULL
);

-- 진단 결과 테이블
CREATE TABLE vibration_diagnosis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_name VARCHAR(50) NOT NULL,
    detected_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fault_type TINYINT NOT NULL CHECK (fault_type IN (0, 1, 2, 3))
        COMMENT '0: 정상, 1: 질량 불균형, 2: 지지 불량, 3: 복합 불량'
);
```

📌 결과 및 의의
실제 사용 데이터 구조에 적합한 테이블로 재설계

AI 학습 및 진단 결과 관리에 최적화된 구조 구성

DB 설계 → 데이터 해석 → AI 결과 반영까지 전체 흐름을 책임지고 수행

해당 DB 구조는 이후 FastAPI 백엔드 서버 및 Next.js 기반 대시보드와 연동되어
AI 기반 진단 시스템의 핵심 데이터 흐름을 담당하게 되었습니다.