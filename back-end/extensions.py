from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

# 확장 모듈 초기화
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()