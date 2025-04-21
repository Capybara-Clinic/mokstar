from flask import Flask
from config import Config
from extensions import db, jwt, ma
from routes.auth import bp as auth_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🔌 Extension 초기화
    register_extensions(app)

    # 🛣️ Blueprint 등록
    register_blueprints(app)

    # 📁 업로드 폴더 생성
    prepare_upload_folder(app)

    return app

def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")

def prepare_upload_folder(app):
    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
