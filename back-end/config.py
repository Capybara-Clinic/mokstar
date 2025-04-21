import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1시간

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")  # ✅ 업로드 경로 설정
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "mp4", "mov", "avi", "webm"}
