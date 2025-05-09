from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from db import Base

# 📌 VibrationData - 설비 진동 수집 데이터 테이블
class VibrationData(Base):
    __tablename__ = "vibration_data"

    id = Column(Integer, primary_key=True, index=True)                       # 고유 ID
    machine_name = Column(String(50), nullable=False, index=True)             # 기계 이름
    sensor_no = Column(String(20), nullable=False, index=True)                # 센서 번호

    collected_at = Column(DateTime, nullable=False)                           # 서버 수집 시각
    measured_time = Column(Float, nullable=False)                             # 센서 기준 측정 시간 (초 단위)

    normal = Column(Float, nullable=False)                                    # 정상 상태 진동값
    unbalance = Column(Float, nullable=False)                                 # 질량 불균형 진동값
    looseness = Column(Float, nullable=False)                                 # 지지 불량 진동값
    unbalance_looseness = Column(Float, nullable=False)                       # 복합 불량 진동값

# 📌 VibrationDiagnosis - 설비 진단 결과 테이블
class VibrationDiagnosis(Base):
    __tablename__ = "vibration_diagnosis"

    id = Column(Integer, primary_key=True, index=True)                        # 고유 ID
    machine_name = Column(String(50), nullable=False, index=True)             # 기계 이름
    detected_at = Column(DateTime, nullable=False)                            # 진단된 시각
    fault_type = Column(TINYINT, nullable=False, comment="0: 정상, 1: 질량 불균형, 2: 지지 불량, 3: 복합 불량")  # 고장 유형
