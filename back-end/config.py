import os
from datetime import timedelta
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    # Flask 기본 설정
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-key')
    
    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLAlchemy 엔진 옵션 (MySQL 8.0+ 인증 문제 해결)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,  # 연결 재활용 시간 (초)
        'pool_timeout': 20,   # 연결 타임아웃 (초)
        'pool_size': 10       # 연결 풀 크기
    }
    
    # JWT 설정
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # 파일 업로드 설정
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 제한