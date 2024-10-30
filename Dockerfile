# Python 이미지를 기반으로 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 프로젝트 소스 코드 복사
COPY . .

# Django 기본 포트 개방
EXPOSE 8000

# Django 개발 서버 시작
CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
