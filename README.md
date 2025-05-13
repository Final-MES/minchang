# 프로젝트 HIM-MES

## 1. 프로젝트 개요 📌

### 1.1 프로젝트명 📁

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

---

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

---

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

### 🧩 문제 파악 및 분석
이후 MLOps 팀 및 수집 데이터 파일을 분석한 결과, 사용 데이터는 회전기계의 진동 데이터를 기반으로 하며, 일부러 고장 상태를 만들어 측정한 센서 값임을 확인했습니다.

📄 진동 수집 데이터셋 주요 컬럼 구성

| 속성 (column) | 설명                                               | 비고   |
|---------------|----------------------------------------------------|--------|
| `Time`        | 데이터의 수집 시간 (측정 기준 시간)                | float |
| `Normal`      | 정상 상태 진동값                                   | float |
| `Type 1`      | 질량 불균형 고장 상태 진동값                       | float |
| `Type 2`      | 지지 불량 고장 상태 진동값                         | float |
| `Type 3`      | 질량 불균형 + 지지 불량 복합 고장 상태 진동값     | float |


📸 센서 데이터 예시
아래는 실제 사용된 회전기계 진동 데이터(g1_sensor1.csv)의 일부입니다.
![센서 데이터 예시](./images/sensor_data_example.png)

또한 AI 진단 결과는 0~3 범위의 숫자로 출력되며, 각각 다음과 같은 상태를 의미합니다:

| 값 (`fault_type`) | 의미         |
|-------------------|--------------|
| `0`               | 정상         |
| `1`               | 질량 불균형  |
| `2`               | 지지 불량    |
| `3`               | 복합 불량    |

### 🛠️ 최종 테이블 설계
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

### 📌 결과 및 의의
실제 사용 데이터 구조에 적합한 테이블로 재설계

AI 학습 및 진단 결과 관리에 최적화된 구조 구성

DB 설계 → 데이터 해석 → AI 결과 반영까지 전체 흐름을 책임지고 수행

해당 DB 구조는 이후 FastAPI 백엔드 서버 및 Next.js 기반 대시보드와 연동되어
AI 기반 진단 시스템의 핵심 데이터 흐름을 담당하게 되었습니다.

## 2. AWS 서버 구성 (RDS, EC2)

### ✅ 많은 클라우드 서비스 중 AWS를 선택한 이유

처음 데이터베이스 구조를 구상하고, 팀원들과 실시간으로 공유하고 테스트할 방법을 고민하던 중  
**클라우드 기반의 데이터베이스 서비스**가 필요하다는 결론에 도달하였습니다.

이를 위해 여러 클라우드 플랫폼(Azure, GCP, Oracle Cloud 등)을 비교해보았고, 다음과 같은 조건을 만족하는 플랫폼이 필요했습니다:

1. **비용이 전혀 들지 않거나, 최소한으로 유지 가능할 것**  
2. **데이터 양(진동 센서 데이터)이 클 경우에도 수 GB~수 TB까지 확장 가능한 구조일 것**

이 중 Oracle Cloud는 "Always Free"라는 이름으로 일부 서비스를 무료 제공하긴 했지만,  
**90일 이상 비활성 시 영구 삭제될 수 있는 정책**을 가지고 있어  
실제 운영이나 장기 테스트 환경에서는 관리에 부담이 있었습니다.

반면 AWS는:

- 최초 가입 시 **1년간 프리 티어 제공**
- **RDS(관계형 DB 서비스)** 및 **EC2(서버 인스턴스)**를 모두 무료 범위 내에서 실습 가능
- 팀원이 동시에 접속해서 API나 대시보드를 테스트하기에 가장 유리

이러한 이유로 AWS의 **프리 티어 기반 RDS + EC2 조합이 가장 실용적**이라고 판단하여 사용하게 되었습니다.

### ✅ RDS를 사용하게 된 이유

데이터베이스 구조를 설계한 뒤, 이를 실제로 테스트하고 팀원들과 공유하려면  
**로컬 환경이 아닌, 외부에서도 접근 가능한 데이터베이스**가 필요했습니다.

처음에는 단순히 `.sql` 파일로 공유하거나, 각자 로컬 DB에 구성해보는 방법도 고려했지만  
- 팀원마다 DB 환경이 다르거나
- 운영체제에 따라 세팅이 번거롭고
- 실시간 협업/검증이 어렵다는 단점이 있었습니다.

그래서 고민 끝에 **클라우드 기반의 데이터베이스 서비스**가 필요하다는 결론에 도달하게 되었고,  
그 중에서도 AWS에서 제공하는 **RDS(Relational Database Service)**는 다음과 같은 장점을 가지고 있었습니다:

- 외부에서도 쉽게 접근 가능 (공용 Endpoint 제공)
- MySQL, PostgreSQL, Oracle 등 다양한 엔진 지원
- 보안 그룹과 IAM 설정을 통해 실무에 가까운 구조 테스트 가능
- FastAPI, Streamlit 등 외부 서버와 쉽게 연동 가능

결론적으로, **RDS를 통해 팀 전체가 동일한 DB 환경에서 협업하고, 실제 운영 환경처럼 API 서버와의 연결을 테스트**할 수 있어  
최종적으로 AWS RDS를 선택하게 되었습니다.

![RDS 인스턴스 관리 화면](./images/aws_rds_dashboard.png)  
> AWS RDS 인스턴스 상태 화면 – MySQL 기반 `him-mes` 데이터베이스

### ✅ EC2를 사용하게 된 이유

처음 팀 프로젝트를 진행하면서, 팀원들과 논의한 결과  
**센서 데이터 외에도 이미지 데이터(예: 설비 상태 이미지)를 수집하고 저장할 필요**가 있다고 판단했습니다.

이때 이미지 데이터를 DB에 직접 저장할 수도 있지만,  
검색을 통해 알게 된 바에 따르면:

- 대용량 이미지 파일을 직접 DB에 저장하는 것은 **성능 저하와 관리 문제**를 유발할 수 있으며,
- 실무에서는 **이미지는 서버에 저장하고, 경로(path)만 DB에 기록하는 방식**을 주로 사용한다는 점을 확인하였습니다.

이러한 구조를 구현하기 위해서는 단순 DB만으로는 부족했고,  
**이미지 파일을 저장할 수 있는 별도의 서버 환경**이 필요했습니다.

그래서 AWS에서 제공하는 **EC2(Elastic Compute Cloud)** 인스턴스를 생성하여,  
**이미지를 저장할 수 있는 파일 서버**로 사용하고자 하였고, 실제로 EC2에 Ubuntu 기반 서버를 구축하여 준비를 진행하였습니다.

그러나 이후 팀 내의 AI 모델 학습을 담당하는 MLOps 팀이 **로컬에서 학습을 진행**하게 되면서,  
이미지 저장 기능은 실제 구현으로 이어지지 않았고,  
EC2는 결과적으로 다음과 같은 용도로 활용되었습니다:

- FastAPI 서버 실행 및 배포
- Swagger 문서 확인, 테스트
- 최종적으로는 Vercel로 이전된 Next.js 대시보드와의 연동 테스트

결론적으로 EC2는 **백엔드 API 서버 및 테스트 환경을 위한 가상 서버로서의 역할**을 성공적으로 수행하였습니다.

![EC2 인스턴스 상태 화면](./images/aws_ec2_instance.png)  
> FastAPI 서버가 배포된 EC2 인스턴스 실행 화면 (`him_EC2`)

### ✅ 예상치 못한 비용 발생의 원인

FastAPI 서버와 MySQL 데이터베이스를 구성하면서 AWS의 **프리 티어 혜택**을 최대한 활용하여  
비용 없이 안정적인 클라우드 환경을 구축하고자 하였습니다.

- EC2와 RDS 인스턴스를 모두 프리 티어 범위 내에서 생성
- 하루 24시간 운영에도 큰 문제가 없다는 점을 사전 확인
- 탄력적 IP(Elastic IP)는 "하나까지는 무료"라는 공식 문서 확인

이런 점들을 바탕으로 "비용이 발생하지 않을 것"이라고 판단하였습니다.

하지만 얼마 지나지 않아 AWS로부터 **비용 청구 알림**을 받게 되었고,  
이로 인해 실제 비용 구조에 대해 **깊이 있게 조사하고 분석하는 계기**가 되었습니다.

---

#### 📌 분석 과정

- 비용이 RDS나 EC2 자체가 아닌, **VPC 네트워크 요금**으로 책정되어 있었음
- 처음에는 **시드니 리전에 실수로 인스턴스를 만들었다가 중지한 이력**이 문제인지 확인
- 이후 AI와 공식 문서 등을 참고하여 확인한 결과:

> **EC2 인스턴스가 계속 켜져 있고, 공인 IP가 연결되어 있다면 탄력적 IP를 사용 중인 것으로 간주됨**  
> 프리 티어 1개 무료는 **정지 상태에서만 무료**이며,  
> **실행 중인 EC2 인스턴스에 연결된 탄력적 IP는 요금 부과 대상이 될 수 있음**

---

### 😓 느낀 점

공식 문서에도 굉장히 작게 기술되어 있는 조건 때문에,  
비용이 발생한 것을 뒤늦게 알아차렸고,  
결국 프로젝트 말미에서야 이를 인지하여 **비용 부담은 개인적으로 감수**하였습니다.

이번 경험을 통해:
- 클라우드 요금은 단순 스펙만이 아니라 **동작 상태, 네트워크 구성까지 확인해야 한다**는 점
- AWS는 처음 접근자에게 다소 **복잡한 요금 정책과 불명확한 UI/UX를 제공**할 수 있다는 점을 체감하였습니다.

하지만 반대로, 이러한 문제를 직접 조사하고 분석하여 원인을 이해하고 정리해낸 경험 자체는  
실무에서의 **문제 해결 능력**과 **클라우드 환경 이해도**를 높일 수 있었던 소중한 기회가 되었습니다.

## 3. FastAPI 구성

### ✅ FastAPI가 필요하다고 판단한 이유

처음 팀 프로젝트에서 데이터베이스 테이블 설계 및 예상 쿼리 작성을 완료한 뒤,  
DB 담당자로서 이후 어떤 역할을 이어나가야 할지 고민하게 되었습니다.
  
저는 그 과정에서 다음과 같은 사실을 알게 되었습니다:

- **DB에 직접 접근하는 ISUD 방식은 보안상 취약할 수 있다**
- 따라서 실제 서비스나 실무에서는 **API를 중간 게이트웨이처럼 두고**  
  DB 접근을 제한하는 구조를 많이 사용한다

이러한 보안적 이유와 실무 흐름에 대한 이해를 바탕으로,  
저도 **API 서버를 구축해보자**는 결정을 내리게 되었습니다.

처음에는 가장 보편적으로 사용되는 **Flask**를 고려했지만,  
당시 팀원이 구성 중인 Docker 환경이 이미 **FastAPI 기반으로 설정되어 있음**을 알게 되었고,  
이에 맞춰 자연스럽게 FastAPI를 선택하게 되었습니다.

FastAPI는:

- **자동 Swagger 문서화**를 지원하여 협업에 용이하고
- **비동기 처리**와 **빠른 응답 속도**
- **경량 REST API 서버 구축에 최적화**

되어 있어, 본 프로젝트에서 필요한 **데이터 송수신 구조 및 보안 게이트웨이** 역할에 적합하다고 판단했습니다.

### ✅ FastAPI의 구성

FastAPI 서버는 최종적으로 진동 수집 데이터와 AI 진단 결과 데이터를 중심으로,  
**읽기(GET)**와 **쓰기(POST)** 기능에 최적화된 REST API 구조로 구성되었습니다.

초기에는 CRUD 중심의 설계였지만, 프로젝트 진행 중 다음과 같은 판단에 따라 구조가 간결해졌습니다:

- 프론트엔드 대시보드에서는 대부분 조회만 필요함
- 진단 결과는 수집 후 분석만 진행하며, 삭제나 수정은 불필요함
- ML 팀과의 데이터 연동은 입력(Bulk), 조회만 있으면 충분함

이에 따라 실제로는 **GET/POST 위주의 목적형 API**로 정리되었고,  
CORS 설정 및 Swagger 문서 자동화를 통해 팀원들과의 테스트 협업도 수월하게 구성하였습니다.

📌 주요 라우팅 구성 예:

- `/vibration-data` (GET, POST, bulk)
- `/vibration-data/grouped-range`: 기계/센서별 범위 내 추출
- `/vibration-diagnosis` (GET, POST, bulk)
- `/vibration-diagnosis/grouped-recent`: 기계별 최근 진단 결과 추출

---

### 📄 Swagger 문서 구성 최적화

API 테스트 및 프론트/ML 연동을 위해 FastAPI가 제공하는 **Swagger UI (`/docs`)** 문서를 적극 활용하였습니다.

특히, 다음과 같은 속성을 각 엔드포인트에 추가하여 **누가 봐도 직관적인 문서**를 구성하였습니다:

- `tags=["진단 결과"]`: 카테고리별 그룹 구분
- `summary="전체 진단 결과 조회"`: 한눈에 이해되는 설명
- `description="..."`: (선택) Swagger 내부에서 상세 설명 제공

```python
@app.get("/vibration-diagnosis", response_model=List[schemas.VibrationDiagnosisRead],
         tags=["진단 결과"], summary="전체 진단 결과 조회")
```

![FastAPI Swagger 문서](images/swagger_ui_example.png)
> FastAPI Swagger 실행 화면

이러한 정리는 프론트엔드 및 머신러닝 팀과의 협업 과정에서  
"API 문서를 따로 만들지 않아도 즉시 이해하고 사용할 수 있었다"는 피드백을 받았고,  
실제 개발 속도를 높이는 데에도 매우 효과적이었습니다.

### ✅ 추가한 기능 (Bulk 등록, 그룹별 조회 등)의 이유

📌 그 중 **Bulk 등록 기능**은 실질적인 문제 해결을 위해 직접 도입한 기능입니다.

진동 수집 데이터는 총 약 **150만 건**, **75MB** 이상의 용량을 가진 대형 CSV 파일이었으며,  
이 데이터를 FastAPI API로 전송하기 위해 처음에는 한 번에 200개씩 나눠 업로드하도록 구성했습니다.

```python
@app.post("/vibration-diagnosis", summary="AI 진단 결과를 등록합니다", tags=["진단 결과"])
def create_diagnosis(diag: schemas.VibrationDiagnosisCreate, db: Session = Depends(get_db)):
    return crud.create_diagnosis(db, diag)
```
그러나 이 방식은 약 8시간 이상 소요되는 비효율적인 처리 시간을 요구했고,
이후 진단 결과 역시 대량 업로드가 필요해짐에 따라 bulk_save_objects() 기반 API를 직접 설계하게 되었습니다.

또한, ML 팀의 결과가 준비되지 않은 상태에서 대시보드 시각화를 테스트하기 위해
진단 결과 더미 데이터를 자동 생성 + 업로드하는 스크립트도 별도로 제작하였습니다.

기계별 고장 유형 확률 분포 구성

특정 날짜(4월 26~27일) 고장률 증가 시뮬레이션

10,000건의 데이터를 POST /vibration-diagnosis/bulk로 전송

```python
upload_batches(generate_dummy_data(10000), batch_size=1000)
```

이때는 이전보다 10배 이상 빠른 속도로 업로드가 가능했으며,
이 경험을 통해 EC2 서버의 안정성, 배치 사이즈 조절의 중요성, 테스트 데이터 생성의 실용성을 모두 체감할 수 있었습니다.

결과적으로 Bulk API는 단순 기능을 넘어서,
대량 데이터 수집 및 테스트 흐름 전반에 필수적인 구조로 발전하게 되었습니다.

📌 추가적으로, 프론트엔드와 연동한 대시보드를 구현하는 과정에서  
단순 전체 데이터 조회(GET)만으로는 기계/센서별 분석과 시각화가 어려웠습니다.

기존 `/vibration-diagnosis` 및 `/vibration-data` 엔드포인트는  
**최신 데이터 1000개 전체를 불러오는 단순 조회 구조**였기 때문에,  
여러 기계(g1 ~ g5), 여러 센서(sensor1 ~ 4) 등으로 분산된 데이터를 **기계별로 나눠 시각화**하거나,  
**센서 조합별로 연속된 시간 그래프를 그리는 데 구조적인 한계**가 있었습니다.

이에 따라 다음과 같은 그룹 기반 조회 API가 도입되었습니다:

- `/vibration-diagnosis/grouped-recent`  
  → 기계별 최근 진단 결과 N개 추출, 시간 정렬 후 `ROW_NUMBER()`로 랭킹 필터링

- `/vibration-data/grouped-range`  
  → 기계+센서 조합별로, 특정 시간 범위(0~140초)의 상위 N개 데이터 추출

해당 API들은 SQL의 `PARTITION BY`, `ROW_NUMBER()` 윈도우 함수를 활용하여  
**기계/센서 기준 데이터 그룹화 + 정렬 + 제한된 개수 추출**을 가능하게 했으며,  
이를 통해 프론트엔드의 시계열 그래프, 최근 진단 요약 등 다양한 기능이 구현될 수 있었습니다.

결과적으로 이 기능들은 단순 조회 이상의 역할을 하며,  
**대시보드 시각화, 기계별 분석, 실시간 데이터 추적 등 고급 기능의 핵심 API**로 자리 잡게 되었습니다.

### ✅ FastAPI의 사용처

FastAPI는 이번 프로젝트에서 **중간 관리자(API 서버)** 역할로 활용되었으며,  
다음과 같은 주요 흐름에서 실질적인 데이터 연동을 담당했습니다:

1. **프론트엔드 대시보드 → DB 조회 (GET)**  
   - Next.js 기반 대시보드에서 FastAPI를 통해 진동 수집 데이터 및 AI 진단 결과를 **선택적으로 불러오기 위한 API** 호출  
   - 그래프 시각화, 기계별 진단 상태 요약 등 UI 구성에 사용

2. **AI 모델 → DB 저장 (POST)**  
   - ML(MLOps) 팀이 학습된 모델의 예측 결과를 FastAPI를 통해 **진단 결과 테이블에 저장**  
   - 단건 또는 bulk 방식 모두 지원하도록 설계되어 있음

즉, FastAPI는 **데이터베이스와 외부 시스템 간의 안전한 통로**로 사용되었으며,  
API 설계, CORS 처리, 데이터 유효성 검증 등 실서비스에 가까운 구조로 운영되었습니다.

## 4. 대시보드

### ✅ Streamlit을 처음 선택하게 된 이유

프로젝트 초기에는 **데이터 시각화와 대시보드 구성**이 핵심 과제 중 하나였으며,  
복잡한 디자인이나 사용자 인터페이스보다는,  
**FastAPI와 연동한 데이터 흐름 테스트 및 시각화 로직 검증**이 주요 목적이었습니다.

이때 선택한 것이 바로 **Streamlit**이었습니다.

Streamlit을 선택한 이유는 다음과 같습니다:

1. **Python 기반의 직관적인 문법**  
   → 별도의 프론트엔드 프레임워크를 배우지 않아도 바로 대시보드 구성 가능

2. **빠른 시각화 구성**  
   → `st.line_chart`, `st.dataframe` 등 기본 컴포넌트를 통해  
      matplotlib/altair 없이도 시계열 그래프, 테이블 등을 빠르게 표현할 수 있음

3. **FastAPI와의 연동 용이**  
   → Python 내에서 직접 `requests.get()` 등을 통해 API 호출하여  
      DB → API → 시각화까지의 흐름을 손쉽게 구성 가능

4. **설치 및 실행이 매우 간단**  
   → `streamlit run app.py` 한 줄로 로컬 테스트 환경 바로 구성 가능

이러한 이유로, 프로젝트 초반에는  
**Streamlit을 통해 API 연동 여부 테스트 및 초기 시각화 구현**에 집중하였으며,  
이는 이후 대시보드의 전체 흐름을 잡는 데 중요한 발판이 되었습니다.

### ✅ Streamlit으로 만들었던 초기 대시보드

Streamlit을 통해 실제로 만든 대시보드는 총 2가지이며,  
FastAPI API 테스트 + 데이터 시각화의 초기 검증용으로 활용되었습니다.

#### 1. 수집 데이터 테이블 출력 (표 형식)
- DB에 저장된 vibration_data 테이블을 조회하여
- 기계명, 센서명, 진동값들을 표 형태로 출력
- 시각화 없이 데이터 확인 및 API 연동 확인 목적

#### 2. 기계/센서별 진동 변화 시계열 그래프

- **X축**: 측정 시간 (measured_time), **Y축**: 진동 수치
- **기계(g1~g5)**, **센서(sensor1~4)** 조합별 데이터 추출
- 필터: 기계 선택, 센서 선택, 다운샘플링 개수, 고장 유형 선택
- **Altair 그래프**를 통해 고장 유형별 색상 구분 시각화

📌 **문제점 & 해결**
- Streamlit 초기 구성 당시 `/vibration-data` API는 최근 1000개 전체 조회 구조
- 이로 인해 기계/센서별로 나눈 데이터가 불균형하게 출력되어 그래프가 깨지는 문제가 발생
- 이후 **기계+센서 조합별 0~140초 내 N개 추출 API** (`/vibration-data/grouped-range`)를 추가하여 해결

![Streamlit 시계열 그래프](images/streamlit_vibration_linechart.png)
> Streamlit 시계열 그래프

🧪 당시 진단 결과 테이블 기반 대시보드도 시도했으나,  
DB에 진단 데이터가 없어서 시각화 시 에러 발생 → 실제로 동작하지 못함

결과적으로 Streamlit 대시보드는 **수집 데이터 시각화 테스트**, **API 구조 설계**,  
**프론트 연동 가능성 검토** 등 다양한 실험의 기반이 되었습니다.

### ✅ Streamlit → Next.js로 변경하게 된 이유

초기에는 Streamlit 기반으로 대시보드를 만들며 테스트를 진행하고 있었으며,  
**EC2에 FastAPI와 함께 올리는 방식**으로 배포를 고려하고 있었습니다.  
실제로 FastAPI는 포트 8000번, Streamlit은 8501번 등으로  
**포트를 분리하여 동시에 운영하는 방법**까지 학습한 상태였습니다.

하지만 이 과정 중 다음과 같은 전환 계기가 발생했습니다:

---

#### 🔄 변경의 계기

- 원래 대시보드를 맡기로 했던 팀원이 개인 사정으로 완성도가 낮을 수 있다고 전달
- 마침 FastAPI까지 마무리된 상황에서 나는 당시에 별다른 작업이 없던 상황에서 대시보드 제작을 하게됨
- 그중 Streamlit을 통해 대시보드를 만들고 있던 도중..
- 팀원들과의 논의 시간에, **다른 팀에서는 Streamlit을 사용하지 않는다**는 이야기를 듣게 됨
- 조사 결과, Streamlit은 다음과 같은 용도로 사용됨을 확인:

| Streamlit의 주요 용도 | 설명 |
| --------------------- | ----- |
| ✅ 실험 및 테스트용 내부 대시보드 | 개발자 간 빠른 확인용 |
| ✅ 데이터 과학자용 분석 시각화 도구 | Pandas/Matplotlib 기반 |
| ❌ 외부 사용자 대상 서비스 | 권장되지 않음 |

---

#### 🚀 Next.js로의 전환 이유

- 현업에서 사용되는 **웹 프론트엔드 프레임워크** 중 `Next.js`가 가장 많이 사용되고 있음
- Streamlit과 달리, Next.js는 **정식 웹 프레임워크 기반**, 대시보드 구축에 적합
- Next.js는 무료 클라우드 호스팅 서비스인 **Vercel**과 연동 가능  
  → **EC2 리소스를 사용하지 않고도 독립적인 프론트 서버 운영 가능**
- **트래픽 분산**, **보안 분리**, **프로젝트 확장성** 측면에서 유리함

---

#### 🔧 판단 요약

- Streamlit은 빠르게 테스트하기에는 최적이지만,
- **실제 서비스 배포에는 Next.js + Vercel 조합이 더 적합**하다고 판단
- GPT를 활용해 구성할 수 있는 점, Vercel 배포의 편리함 등이 전환의 결정적 요인이 됨

---

이러한 흐름을 통해 프로젝트 후반부 대시보드는 Streamlit → Next.js로 전환되었으며,  
이후 전체 시스템 구성에서 프론트엔드와 백엔드의 분리, 유지보수성 향상에 도움이 되었습니다.

### 4. 만든 Next.js 대시보드 구성

프로젝트 후반부, Streamlit에서 Next.js로 대시보드 구성을 전환한 뒤
실제로 제가 만들어 Vercel에 배포하여 운영한 페이지는 총 3가지입니다.

각 대시보드는 FastAPI 백엔드와 연동되어 실시간 데이터를 시각화하거나
AI 진단 결과를 분석하여 프론트엔드에 표시하는 구조로 이루어져 있습니다.

#### 📊 1. 진동 데이터 테이블 (vibration-table)
- 주소: https://him-mes-vercel.vercel.app/vibration-table

- 설명:
  기계(g1g5), 센서(sensor14)별로 수집된 진동 데이터를 표 형태로 확인할 수 있는 페이지입니다.

- 기능 요약:

  - 기계명/센서번호 필터
  - 1000개 최신 데이터 출력
  - 진동 수치 (정상 / 질량 불균형 / 지지 불량 / 복합 고장) 확인

![1. 진동 데이터 테이블](images/nextjs_vibration_table.png)
> 1. 진동 데이터 테이블

#### 🛠️ 2. 진단 결과 대시보드 (diagnosis-dashboard)
- 주소: https://him-mes-vercel.vercel.app/diagnosis-dashboard

- 설명:
  각 기계별 최근 AI 진단 결과를 표 형태로 정리하여 한눈에 상태를 파악할 수 있게 구성한 대시보드입니다.

- 기능 요약:

  - 날짜 범위 선택 필터
  - 기계명 버튼 클릭 필터
  - 고장/정상 상태 및 고장 유형 시각적 구분

![2. 진단 결과 대시보드](images/nextjs_diagnosis_dashboard.png)
> 2. 진단 결과 대시보드


#### 📈 3. 고장 진단 시계열 (machine-fault-timeline)
- 주소: https://him-mes-vercel.vercel.app/machine-fault-timeline

- 설명:
  시간 흐름에 따라 기계별로 어떤 고장이 발생했는지 시각적으로 나타내는 시계열 분석 그래프입니다.

- 기능 요약:

  - 진단 시각 기준 시간 축 정렬
  - 고장 유형별 색상 영역 강조 (정상/불균형/지지 불량/복합)
  - 여러 기계의 시계열 비교 가능

![3. 고장 진단 시계열](images/nextjs_fault_timeline.png)
> 3. 고장 진단 시계열

📌 참고
본 대시보드는 Next.js + Recharts 조합으로 구현되었으며,
Vercel 플랫폼을 이용해 무료 배포되었습니다.
이로써 EC2와의 리소스 충돌을 피하고, 트래픽 분산 및 빠른 로딩 속도를 확보할 수 있었습니다.

### 🛠️ Next.js 대시보드의 타이틀 문제 해결 과정
프로젝트 발표 이후, 팀 리더님으로부터
각 대시보드 페이지의 상단 탭 제목(title)이 모두 동일하게 "Create Next App"으로 표시되고 있다는 피드백을 받았습니다.

#### ⚠️ 문제 상황
Next.js의 기본 구조에서는 /src/app/layout.tsx 내에 설정된 metadata가
모든 하위 페이지에 동일하게 적용되어, 각 대시보드 페이지의 **탭 타이틀(title)**이 동일하게 표시되는 문제가 있었습니다.
| 기본 타이틀 (수정 전) | ![기본 상태](images/nextjs_default_tab_title.png) |
```tsx
export const metadata: Metadata = {
  title: "스마트팩토리 MES 대시보드",
  description: "MES 기반의 진단 시각화 플랫폼입니다.",
};
```
이 구조에서는 모든 하위 페이지(/vibration-table, /diagnosis-dashboard, /machine-fault-timeline)가 동일한 제목을 가지게 됨

결과적으로, 각 대시보드의 목적이 다른데도 불구하고
브라우저 탭에 동일한 제목이 표시되어 혼동이 발생

#### 🔍 해결 방안 탐색
page.tsx에서 use client 환경에서는 export const metadata 사용이 불가
반대로 서버 사이드에서만 사용하는 경우, 기존 클라이언트 컴포넌트를 활용할 수 없음

#### ✅ 최종 구조 및 설정 방법

📁 각 대시보드 폴더 구성 예시 (machine-fault-timeline 기준)
```arduino
/src/app/machine-fault-timeline/
├── page.tsx         ← metadata 설정 및 Client 컴포넌트 호출
├── layout.tsx       ← 최소 레이아웃 유지
└── Client.tsx       ← 실제 대시보드 UI 구성
```
1. `Client.tsx` – 클라이언트 컴포넌트 분리
```tsx
// src/app/machine-fault-timeline/Client.tsx
'use client';

export default function MachineFaultTimelineClient() {
  return (
    <div>여기에 기존 대시보드 구성 요소 출력</div>
  );
}
```
> 👉 대시보드 UI 로직 및 상호작용이 포함된 컴포넌트

2. `page.tsx` – Metadata 설정 및 Client 호출
```tsx
// src/app/machine-fault-timeline/page.tsx
import { Metadata } from 'next';
import MachineFaultTimelineClient from './Client';

export const metadata: Metadata = {
  title: '고장 진단 시계열',
  description: '기계별 고장 상태를 시간 순으로 분석하는 페이지입니다',
};

export default function Page() {
  return <MachineFaultTimelineClient />;
}
```
> 👉 각 페이지별 탭 타이틀과 설명을 개별적으로 정의 가능

3. `layout.tsx` – 최소한의 HTML 구조 유지
```tsx
// src/app/machine-fault-timeline/layout.tsx
import React from 'react';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
```
> 👉 별도 공통 레이아웃이 필요 없는 경우, 최소한의 구조로 구성

#### ✅ 적용 결과
각 대시보드의 상단 탭(title)이 다음과 같이 개별 설정 가능해졌습니다:

| 페이지 경로               | 탭 타이틀             |
|--------------------------|------------------------|
| `/vibration-table`       | 진동 데이터 테이블     |
| `/diagnosis-dashboard`   | 진단 대시보드          |
| `/machine-fault-timeline`| 고장 진단 시계열        |

> 각 페이지별 타이틀 분리 (수정후)

![분리된 상태](images/nextjs_custom_tab_titles.png)

이와 같은 구조를 통해
각 페이지마다 독립된 탭 제목 설정이 가능해졌으며,
브라우저 탭, 북마크, 검색엔진 최적화(SEO) 등에도 긍정적인 영향을 줄 수 있습니다. ✅

### 5. Vercel을 통한 대시보드 배포
#### ✅ 1. 배포 방식 및 절차
최종적으로 완성한 Next.js 기반 대시보드는 Vercel 플랫폼을 통해 무료로 배포하였습니다.

Vercel은 Next.js 공식 배포 플랫폼으로, 다음과 같은 특징이 있습니다:

  - GitHub 연동을 통한 자동 배포

  - 기본 HTTPS 제공

  - 무료 요금제 기준에서도 빠른 속도 제공

  - 커스텀 도메인 설정 가능

🛠️ 배포 절차 요약
  1. https://vercel.com 접속

  2. GitHub 계정으로 로그인

  3. 배포할 Next.js 프로젝트가 포함된 GitHub 레포지토리 선택

  4. 배포 설정 없이 기본 상태로 "Deploy" 버튼 클릭

  5. 수 초 내로 배포 완료 → .vercel.app 주소 자동 생성

📌 별도의 EC2, Docker 설정 없이도
정적/동적 웹 대시보드를 빠르게 운영할 수 있는 것이 큰 장점입니다.

#### ✅ 2. 사용 방법 및 접근 방식
아래는 Vercel에 배포된 Next.js 대시보드 각각의 페이지별 주소입니다:

| 대시보드 이름 | 설명 | 접속 링크 |
|---------------|------|------------|
| 진동 데이터 테이블 | 수집된 진동 데이터를 기계/센서별로 필터링하여 표 형태로 시각화 | [vibration-table](https://him-mes-vercel.vercel.app/vibration-table) |
| 진단 결과 대시보드 | 각 기계의 최근 AI 진단 결과를 표로 표시 | [diagnosis-dashboard](https://him-mes-vercel.vercel.app/diagnosis-dashboard) |
| 고장 진단 시계열 | 시간 흐름에 따라 기계별 고장 유형 변화를 시계열 그래프로 표현 | [machine-fault-timeline](https://him-mes-vercel.vercel.app/machine-fault-timeline) |

브라우저 주소창에 해당 주소를 입력하거나 클릭하면 누구나 접근할 수 있으며,  
FastAPI API 서버와 연동되어 실시간 데이터를 표시합니다.

![Vercal 서버 이미지](images/vercel_deployment_status.png)
> 실제 운영 중인 Vercel 배포 상태 확인 화면

📌 참고 사항
해당 대시보드는 Next.js + Recharts 기반으로 구성되어 있으며,

백엔드는 EC2에 배포된 FastAPI 서버를 통해 진동 데이터 및 진단 결과를 수신합니다.

FastAPI에는 CORS, 데이터 유효성 검증 등의 처리가 사전 구성되어 있어,
프론트엔드는 fetch() 기반으로 안정적으로 API 호출 및 데이터 표시가 가능합니다.

### 6. MFC – Next.js 연동
#### ✅ 연동 필요 배경

프로젝트에서 MFC 기반의 스마트팩토리 통합 대시보드 GUI가 이미 구현된 상황이었으며,
그 안에서 별도로 내가 만든 Next.js 웹 대시보드 화면을 통합하는 것이 요구되었음.

![MFC 기본 대시보드 프레임](images/mfc_dashboard_frame.png)
> MFC로 구현된 대시보드 기본 화면

#### ✅ 고려한 연동 방법
연동 방식은 크게 다음 두 가지를 비교·고려하였음:

| 방법 | 설명 |
|------|------|
| **① WebView2** | MFC 창 내부에 브라우저 엔진을 삽입하여 Next.js 화면을 내장 |
| **② 링크 클릭 → 브라우저 열기** | 버튼 클릭 시 외부 브라우저에서 Next.js 페이지를 새 창으로 열기 |

#### ✅ 최종 선택: 외부 브라우저 연동 방식 (방법②)
WebView2는 초기 설정 및 버전 호환 문제 등으로 시간이 많이 소요될 수 있었음

발표 및 시연 일정이 촉박했던 상황에서 빠르고 확실하게 연동 가능한 방식이 필요했음

이에 따라 MFC에서 버튼 클릭 시 ShellExecute()로 Vercel 배포 주소를 여는 방식을 채택함

```cpp
ShellExecute(0, NULL, _T("https://him-mes-vercel.vercel.app/vibration-table"), NULL, NULL, SW_SHOWNORMAL);
```
#### ✅ 연동 결과 및 장점

빠르게 브라우저에서 완성된 대시보드를 열 수 있어 팀 발표 및 테스트에 적합

Vercel에서 호스팅된 Next.js 페이지이기 때문에 EC2 서버 자원 부담 없음

추후 WebView2로 내부 탭화 구현 시에도 동일 주소 기반이므로 확장 가능

---

## 7. 프로젝트 결과 및 회고

### 🗓️ 프로젝트 기간 및 역할
- 기간: 2025년 4월 14일 ~ 5월 9일
- 역할: 데이터베이스 구조 설계, API 서버 구축, 대시보드 시각화 및 연동

### 🚧 가장 어려웠던 점
- 150만건 이상의 대형 CSV 데이터 업로드 시, API 성능 저하 및 중복 업로드 문제 발생
- Streamlit에서의 시각화 제한 → Next.js로 전환 과정에서 탭 타이틀 분리 문제 등
- AWS 비용 발생 문제 찾기

### 💡 해결 방법 및 성과
- FastAPI에 Bulk 등록 API 및 그룹별 조회 API 도입 → 속도 10배 개선
- 진동 수집 / 진단 데이터 구조를 정규화하여 안정적 분석 기반 마련
- Next.js 대시보드 → Vercel 무료 배포로 EC2 리소스 분산 및 안정적 운영 성공

### 📈 배운 점
- 실제 클라우드 환경(AWS)에서의 배포/요금 관리 경험
- RESTful API의 구조화 설계 및 Swagger 문서화 능력 향상
- Recharts 및 Front-Back 연동 구조 경험을 통해 프론트 역량 일부 습득

---

















