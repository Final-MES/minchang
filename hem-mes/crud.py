from sqlalchemy.orm import Session
from models import VibrationData, VibrationDiagnosis
import schemas
from typing import Optional

# 📌 VibrationData - 설비 진동 수집 데이터

def create_vibration_data(db: Session, data: schemas.VibrationDataCreate):
    db_data = VibrationData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return {"status": "success", "data": db_data}

def get_all_vibration_data(db: Session):
    return db.query(VibrationData).order_by(VibrationData.machine_name).all()

def get_vibration_data_by_id(db: Session, data_id: int) -> Optional[VibrationData]:
    return db.query(VibrationData).filter(VibrationData.id == data_id).first()

def update_vibration_data(db: Session, data_id: int, updated: schemas.VibrationDataCreate):
    db_data = get_vibration_data_by_id(db, data_id)
    if db_data:
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(db_data, key, value)
        db.commit()
        db.refresh(db_data)
        return {"status": "success", "data": db_data}
    return {"status": "error", "detail": "Vibration data not found."}

def delete_vibration_data(db: Session, data_id: int):
    db_data = get_vibration_data_by_id(db, data_id)
    if db_data:
        db.delete(db_data)
        db.commit()
        return {"status": "success", "detail": "Vibration data deleted."}
    return {"status": "error", "detail": "Vibration data not found."}

# 📌 VibrationDiagnosis - 진단 결과

def create_diagnosis(db: Session, diag: schemas.VibrationDiagnosisCreate):
    db_diag = VibrationDiagnosis(**diag.dict())
    db.add(db_diag)
    db.commit()
    db.refresh(db_diag)
    return {"status": "success", "data": db_diag}

def get_all_diagnoses(db: Session):
    return db.query(VibrationDiagnosis).order_by(VibrationDiagnosis.machine_name).all()

def get_diagnosis_by_id(db: Session, diag_id: int) -> Optional[VibrationDiagnosis]:
    return db.query(VibrationDiagnosis).filter(VibrationDiagnosis.id == diag_id).first()

def update_diagnosis(db: Session, diag_id: int, updated: schemas.VibrationDiagnosisCreate):
    db_diag = get_diagnosis_by_id(db, diag_id)
    if db_diag:
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(db_diag, key, value)
        db.commit()
        db.refresh(db_diag)
        return {"status": "success", "data": db_diag}
    return {"status": "error", "detail": "Diagnosis data not found."}

def delete_diagnosis(db: Session, diag_id: int):
    db_diag = get_diagnosis_by_id(db, diag_id)
    if db_diag:
        db.delete(db_diag)
        db.commit()
        return {"status": "success", "detail": "Diagnosis data deleted."}
    return {"status": "error", "detail": "Diagnosis data not found."}