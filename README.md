# 프로젝트 HIM-MES

## 1. 프로젝트 개요 📌

### 📁 프로젝트명

스마트 팩토리 MES(Manufacturing Execution System) 프로젝트

### 📝 프로젝트 설명

모듈형 MES 공정 데이터 파이프라인 설계 프로젝트입니다.
데이터 분석이 아닌, 데이터 기반 의사 결정 인프라를 구축하는 데 중점을 두었습니다.

## 참여자
- 김민창 (DB/백엔드/대시보드)
- 지평진, 고찬국, 김사무엘, 송창우

---

## 2. 내가 맡은 역할 ✍ # minchang

### ☁️ 클라우드 서버 관리
- AWS EC2 인스턴스를 이용한 FastAPI 서버 호스팅
- Docker를 활용한 FastAPI 컨테이너화 및 자동화 배포
- AWS RDS(MySQL) 연동 및 보안 그룹, 포트 설정 최적화

### 🗄️ DB 설계 및 관리
- MySQL 기반 진동 수집 및 진단 테이블 스키마 설계
- SQLAlchemy를 활용한 ORM 매핑 및 데이터 모델링
- `measured_time` 기반 대용량 데이터 저장 및 조회 쿼리 최적화
- 150만 건 이상 진동 데이터를 중복 검사 및 자동 업로드 스크립트 구현

### 🔧 API 개발 및 관리
- FastAPI 기반 RESTful API 설계 및 구현
- `/vibration-data`, `/vibration-diagnosis` 등 핵심 진동 데이터 관리 API 개발
- 기계별 최근 진단 데이터 조회용 고급 SQL 서브쿼리 및 응답 구조 설계
- Swagger 문서 자동화 및 팀원 테스트 환경 제공

### 🎨 대시보드 제작
- Streamlit 기반 진동 파형 시각화 대시보드 개발 (초기 테스트용)
- Vercel에 배포된 Next.js 기반 진단 결과 시계열 대시보드 제작
- Recharts, Chart.js 등 라이브러리를 활용한 실시간 고장 히스토리 시각화
- 사용자 필터(기계명, 날짜, 상태 유형) 및 커스텀 툴팁 UI 구성

---

## 3. 🧰 사용 기술 스택

### 🔙 백엔드 / 서버
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF6F00?style=flat)

### 🧮 데이터베이스
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![AWS RDS](https://img.shields.io/badge/AWS%20RDS-527FFF?style=flat&logo=amazonaws&logoColor=white)

### 🎨 대시보드 / 프론트엔드
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white)

### ☁️ 클라우드 / 배포
![AWS EC2](https://img.shields.io/badge/AWS%20EC2-FF9900?style=flat&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white)

### 🔧 개발 도구
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)

---

## 📷 4. 주요 결과 화면

### 🧱 1. 최종 DB 테이블 스키마

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

### 🖥️ 2. AWS RDS 및 EC2 콘솔

![RDS 인스턴스 관리 화면](./images/aws_rds_dashboard.png)  
> AWS RDS 인스턴스 상태 화면 – MySQL 기반 `him-mes` 데이터베이스

![EC2 인스턴스 상태 화면](./images/aws_ec2_instance.png)  
> FastAPI 서버가 배포된 EC2 인스턴스 실행 화면 (`him_EC2`)

### 🔗 3. Swagger 자동 문서화 화면
FastAPI의 /docs 엔드포인트를 통해 자동 생성된 Swagger 문서입니다.
각 API의 엔드포인트, 메서드(GET/POST), 파라미터, 응답 예시 등을 직관적으로 확인할 수 있습니다.

![FastAPI Swagger 문서](images/swagger_ui_example.png)
> Swagger 문서 자동화 결과 (FastAPI `/docs` 화면)

### 📊 4. 배포된 대시보드 화면
| 페이지명       | 설명               | 링크                                                                           | 이미지                                               |
| ---------- | ---------------- | ---------------------------------------------------------------------------- | ------------------------------------------------- |
| 진동 데이터 테이블 | 진동 데이터 필터링 및 확인  | [vibration-table](https://him-mes-vercel.vercel.app/vibration-table)         | ![vibration](images/nextjs_vibration_table.png) |
| 진단 결과 대시보드 | 기계별 진단 상태 요약 시각화 | [diagnosis-dashboard](https://him-mes-vercel.vercel.app/diagnosis-dashboard) | ![diag](images/nextjs_diagnosis_dashboard.png)  |
| 고장 진단 시계열  | 시간 흐름에 따른 고장 변화  | [fault-timeline](https://him-mes-vercel.vercel.app/machine-fault-timeline)   | ![fault](images/nextjs_fault_timeline.png)      |


## 5. 프로젝트 결과 및 회고

### 🗓️ 프로젝트 기간 및 담당 역할

- **기간**: 2025년 4월 14일 ~ 5월 9일
- **담당**: 데이터베이스 구조 설계, FastAPI 기반 API 서버 구축, Next.js 대시보드 개발 및 연동

### 🚧 가장 어려웠던 점

- 약 **150만 건 이상의 대형 CSV 데이터 업로드** 시
→ API 성능 저하, 중복 처리 문제 발생

- Streamlit 사용 중 시각화 한계 및 API 구조 미흡
→ **Next.js 전환 후에도 탭 타이틀 분리 등 기술적 이슈** 발생

- AWS 환경에서의 **비용 청구 문제**
→ 탄력적 IP 요금, VPC 네트워크 비용 등 예상 외 지출 발생

### 💡프로젝트 성과

- **✅ FastAPI Bulk API 도입**
→ 데이터 업로드 속도 약 10배 향상 (200개 단위 → 1000개 단위 처리)

- **✅ 데이터 구조 정규화**
→ 진동 수집 데이터와 진단 데이터를 안정적 분석 가능 형태로 재설계

- **✅ Next.js 대시보드 + Vercel 배포 구조로 전환**
→ 프론트/백 분리 및 EC2 리소스 분산, 운영 안정성 확보

### 📈 프로젝트를 통해 배운 점

- ☁️ **클라우드(AWS) 요금 구조에 대한 실전 경험**
→ 탄력 IP/VPC 비용 등 예상치 못한 리스크 학습

- 🧩 **RESTful API 구조 설계 및 문서화 경험**
→ Swagger를 통한 테스트 및 팀원 협업 효율 개선

- 💻 **프론트엔드와 백엔드 연동 구조에 대한 이해 향상**
→ Recharts, fetch API, CORS 처리 등 실전 기반 기술 습득

#### 📌 회고 요약:
이번 프로젝트는 단순한 기술 구현을 넘어서,
**데이터 흐름 설계, 협업, 실서비스 시뮬레이션, 비용 분석**까지
모두 체감하고 학습할 수 있었던 **종합 실무 경험의 기회, 앞으로의 개발자로서의 성장 기반이 되었습니다.**