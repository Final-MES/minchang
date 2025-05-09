# 📈 FastAPI 진동 데이터 + 진단 결과 API (알파벳순 정렬 수정본)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import SessionLocal, engine, Base
import models, schemas, crud
from typing import List
from sqlalchemy.exc import IntegrityError

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MES 진동 분석 API",
    description="설비 + 센서 + AI 진단 연동 API",
    version="1.0.0"
)

# 🔵 CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 세션

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 기본 동작 확인

@app.get("/", summary="API 서버 동작 확인", tags=["서버 상태"])
def root():
    return {"message": "FastAPI 서버 정상 동작 중"}

# 📌 [1] 진단 결과 데이터 (vibration_diagnosis)

@app.get("/vibration-diagnosis", response_model=List[schemas.VibrationDiagnosisRead], tags=["진단 결과"], summary="전체 진단 결과 조회")
def get_all_diagnosis_data(db: Session = Depends(get_db)):
    data = db.query(models.VibrationDiagnosis).filter(models.VibrationDiagnosis.detected_at != None).order_by(models.VibrationDiagnosis.machine_name).all()
    if not data:
        raise HTTPException(status_code=404, detail="No diagnosis data found.")
    return data

@app.get("/vibration-diagnosis/grouped-recent", response_model=List[schemas.VibrationDiagnosisRead], tags=["진단 결과"], summary="기계별 최근 N개의 진단 결과 추출")
def get_grouped_diagnosis_data_recent(per_group_limit: int = 1000, db: Session = Depends(get_db)):
    raw_sql = text("""
        SELECT * FROM (
            SELECT *, ROW_NUMBER() OVER (
                PARTITION BY machine_name ORDER BY detected_at DESC
            ) AS rn
            FROM vibration_diagnosis
        ) AS sub
        WHERE rn <= :per_group_limit
        ORDER BY machine_name, detected_at DESC
    """)
    results = db.execute(raw_sql, {"per_group_limit": per_group_limit}).mappings().all()
    return results

@app.post("/vibration-diagnosis", summary="AI 진단 결과를 등록합니다", tags=["진단 결과"])
def create_diagnosis(diag: schemas.VibrationDiagnosisCreate, db: Session = Depends(get_db)):
    return crud.create_diagnosis(db, diag)

@app.post("/vibration-diagnosis/bulk", summary="다중 진단 결과 등록", tags=["진단 결과"])
def create_bulk_diagnosis_data(data_list: List[schemas.VibrationDiagnosisCreate], db: Session = Depends(get_db)):
    objs = [models.VibrationDiagnosis(**data.dict()) for data in data_list]
    db.bulk_save_objects(objs)
    db.commit()
    return {"status": "success", "inserted": len(objs)}

# 📌 [2] 진동 데이터 (vibration_data)

@app.get("/vibration-data", response_model=List[schemas.VibrationDataRead], tags=["진동 데이터"], summary="0~140초 내 전체 진동 데이터 조회")
def get_all_vibration_data(db: Session = Depends(get_db)):
    data = db.query(models.VibrationData).filter(models.VibrationData.measured_time <= 140).order_by(models.VibrationData.machine_name).all()
    if not data:
        raise HTTPException(status_code=404, detail="No vibration data found.")
    return data

@app.get("/vibration-data/grouped-range", response_model=List[schemas.VibrationDataRead], tags=["진동 데이터"], summary="기계/센서 조합별 0~140초 내 최대 N개 추출")
def get_grouped_vibration_data_range(per_group_limit: int = 1000, db: Session = Depends(get_db)):
    raw_sql = text("""
        SELECT * FROM (
            SELECT *, ROW_NUMBER() OVER (
                PARTITION BY machine_name, sensor_no ORDER BY measured_time
            ) AS rn
            FROM vibration_data
            WHERE measured_time BETWEEN 0 AND 140
        ) AS sub
        WHERE rn <= :per_group_limit
        ORDER BY machine_name, sensor_no, measured_time
    """)
    results = db.execute(raw_sql, {"per_group_limit": per_group_limit}).mappings().all()
    return results

@app.post("/vibration-data", summary="센서 진동 데이터를 등록합니다", tags=["진동 데이터"])
def create_vibration_data(data: schemas.VibrationDataCreate, db: Session = Depends(get_db)):
    return crud.create_vibration_data(db, data)

@app.post("/vibration-data/bulk", summary="다중 진동 데이터 등록", tags=["진동 데이터"])
def create_bulk_vibration_data(data_list: List[schemas.VibrationDataCreate], db: Session = Depends(get_db)):
    objs = [models.VibrationData(**data.dict()) for data in data_list]
    db.bulk_save_objects(objs)
    db.commit()
    return {"status": "success", "inserted": len(objs)}
