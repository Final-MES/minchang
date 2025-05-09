# db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import settings  # settings.py를 불러온다

# DB 연결 URL 구성
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# SQLAlchemy 엔진 및 세션 생성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 베이스 클래스
Base = declarative_base()

# DB 세션 생성용 함수 (FastAPI Depends에 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
