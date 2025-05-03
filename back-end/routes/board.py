from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.file import allowed_file, save_file
from extensions import db
from models.board import Board
from schemas.board import board_schema, boards_schema
from sqlalchemy import desc

bp = Blueprint("board", __name__, url_prefix="/board")

@bp.route("", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    title = request.form.get("title")
    content = request.form.get("content")
    
    # 파일 업로드 코드는 모델에 file_path 필드가 없어서 주석 처리
    # file = request.files.get("file")
    # file_path, file_type = None, None
    # if file:
    #     if not allowed_file(file.filename, file.mimetype):
    #         return jsonify({"msg": "허용되지 않은 파일 형식"}), 400
    #     file_path, file_type = save_file(file)

    post = Board(
        user_id=user_id,
        title=title,
        content=content,
        # file_path=file_path,
        # file_type=file_type,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({"msg": "게시글 등록 완료", "post": board_schema.dump(post)}), 201

@bp.route("", methods=["GET"])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    posts = Board.query.order_by(desc(Board.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    result = boards_schema.dump(posts.items)
    return jsonify(result), 200

@bp.route("/<int:board_id>", methods=["GET"])
def get_post(board_id):
    post = Board.query.get_or_404(board_id)
    
    # 조회수 증가 코드는 모델에 view_cnt 필드가 없어서 주석 처리
    # post.view_cnt += 1
    # db.session.commit()
    
    result = board_schema.dump(post)
    return jsonify(result), 200

@bp.route("/<int:board_id>", methods=["PUT"])
@jwt_required()
def update_post(board_id):
    user_id = get_jwt_identity()
    post = Board.query.get_or_404(board_id)
    
    # 작성자 확인
    if post.user_id != user_id:
        return jsonify({"msg": "권한이 없습니다"}), 403
    
    # JSON 또는 form-data 처리
    if request.is_json:
        data = request.json
        title = data.get("title")
        content = data.get("content")
    else:
        title = request.form.get("title")
        content = request.form.get("content")
    
    # 데이터 업데이트
    if title:
        post.title = title
    if content:
        post.content = content
    
    db.session.commit()
    return jsonify({"msg": "게시글이 수정되었습니다"}), 200

@bp.route("/<int:board_id>", methods=["DELETE"])
@jwt_required()
def delete_post(board_id):
    user_id = get_jwt_identity()
    post = Board.query.get_or_404(board_id)
    
    # 작성자 확인
    if post.user_id != user_id:
        return jsonify({"msg": "권한이 없습니다"}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({"msg": "게시글이 삭제되었습니다"}), 200