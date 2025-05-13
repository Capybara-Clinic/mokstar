from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db, jwt, bcrypt, ma
from routes.auth import auth_bp
from routes.board import board_bp
from routes.comment import comment_bp
import os
from models import User, BulletinBoard, Comment

def create_app(config_class=Config):
    # Flask 앱 초기화
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # CORS 설정
    CORS(app)
    
    # 확장 모듈 초기화
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    
    # 마이그레이션 설정
    Migrate(app, db)
    
    # 업로드 폴더 생성
    uploads_dir = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(uploads_dir, exist_ok=True)
    
    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(board_bp)
    app.register_blueprint(comment_bp)
    
    # URL 규칙 추가 (업로드 폴더 접근)
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app

# 앱 생성
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)