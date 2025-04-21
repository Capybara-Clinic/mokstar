from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data["pw"])

    user = User(
        user_id=data["user_id"],
        pw=hashed_pw,
        email=data["email"],
        nickname=data["nickname"]
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.user_id)
    return jsonify({
        "access_token": access_token,
        "user": {
            "user_id": user.user_id,
            "nickname": user.nickname
        }
    }), 201
