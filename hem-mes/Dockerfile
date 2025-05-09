# Dockerfile

FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 현재 디렉토리의 모든 파일을 컨테이너에 복사
COPY . /app

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 8000 포트 오픈
EXPOSE 8000

# uvicorn으로 FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
