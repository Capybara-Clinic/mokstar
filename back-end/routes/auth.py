from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from utils.security import hash_password, verify_password
from flask_jwt_extended import create_access_token
from schemas.user import user_schema

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(user_id=data["user_id"]).first():
        return jsonify({"msg": "이미 존재하는 ID"}), 400

    user = User(
        user_id=data["user_id"],
        pw=hash_password(data["pw"]),
        email=data["email"],
        nickname=data["nickname"]
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.user_id)
    return jsonify(access_token=token, user=user_schema.dump(user)), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(user_id=data["user_id"]).first()
    if not user or not verify_password(user.pw, data["pw"]):
        return jsonify({"msg": "로그인 실패"}), 401

    token = create_access_token(identity=user.user_id)
    return jsonify(access_token=token, user=user_schema.dump(user)), 200
