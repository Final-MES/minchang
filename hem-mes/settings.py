# settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # FastAPI 기본 세팅
    PROJECT_NAME: str = "MES 진동 분석 API"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # DB 연결 설정
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = ".env"  # 루트에 있는 .env 파일을 자동으로 읽음

# 인스턴스 생성
settings = Settings()
