
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.file import allowed_file, save_file
from extensions import db
from models.board import BulletinBoard  # 너 DB에 맞춰 모델 구성 필요

bp = Blueprint("board", __name__, url_prefix="/board")

@bp.route("", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    title = request.form.get("title")
    content = request.form.get("content")
    file = request.files.get("file")

    file_path, file_type = None, None

    if file:
        if not allowed_file(file.filename, file.mimetype):
            return jsonify({"msg": "허용되지 않은 파일 형식"}), 400
        file_path, file_type = save_file(file)

    post = BulletinBoard(
        user_id=user_id,
        title=title,
        content=content,
        file_path=file_path,
        file_type=file_type,
        view_cnt=0
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({"msg": "게시글 등록 완료"}), 201
