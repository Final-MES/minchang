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











