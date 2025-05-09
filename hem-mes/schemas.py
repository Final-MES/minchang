from pydantic import BaseModel, Field
from datetime import datetime

# 📌 1. 진동 수집 데이터용

class VibrationDataCreate(BaseModel):
    machine_name: str = Field(..., example="Machine_A")
    sensor_no: str = Field(..., example="Sensor_01")
    collected_at: datetime = Field(..., example="2025-04-29T12:34:56")
    measured_time: float = Field(..., example=12.345)
    normal: float = Field(..., example=0.012)
    unbalance: float = Field(..., example=0.034)
    looseness: float = Field(..., example=0.056)
    unbalance_looseness: float = Field(..., example=0.078)

    class Config:
        orm_mode = True

class VibrationDataRead(VibrationDataCreate):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True

# 📌 2. 진단 결과 데이터용

class VibrationDiagnosisCreate(BaseModel):
    machine_name: str = Field(..., example="Machine_A")
    detected_at: datetime = Field(..., example="2025-04-29T12:45:00")
    fault_type: int = Field(..., example=2, description="0: 정상, 1: 질량 불균형, 2: 지지 불량, 3: 복합 불량")

    class Config:
        orm_mode = True

class VibrationDiagnosisRead(VibrationDiagnosisCreate):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True
