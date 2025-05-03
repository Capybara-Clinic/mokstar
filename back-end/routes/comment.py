from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.comment import Comment
from models.board import Board
from schemas.comment import comment_schema, comments_schema

bp = Blueprint("comments", __name__)

@bp.route("/board/<int:board_id>/comments", methods=["POST"])
@jwt_required()
def create_comment(board_id):
    user_id = get_jwt_identity()
    data = request.json
    
    # 게시글 존재 확인
    post = Board.query.get_or_404(board_id)
    
    # pre_comid 필드가 모델에 없어서 주석 처리
    # pre_comid = data.get("pre_comid")
    # if pre_comid:
    #     parent_comment = Comment.query.get(pre_comid)
    #     if not parent_comment or parent_comment.board_id != board_id:
    #         return jsonify({"msg": "잘못된 부모 댓글입니다"}), 400
    
    comment = Comment(
        user_id=user_id,
        board_id=board_id,
        content=data["content"],
        # pre_comid=pre_comid
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify(comment_schema.dump(comment)), 201

@bp.route("/board/<int:board_id>/comments", methods=["GET"])
def get_comments(board_id):
    # 게시글 존재 확인
    Board.query.get_or_404(board_id)
    
    comments = Comment.query.filter_by(board_id=board_id).order_by(Comment.created_at).all()
    result = comments_schema.dump(comments)
    
    return jsonify(result), 200

@bp.route("/comments/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get_or_404(comment_id)
    
    # 작성자 확인
    if comment.user_id != user_id:
        return jsonify({"msg": "권한이 없습니다"}), 403
    
    data = request.json
    comment.content = data["content"]
    
    db.session.commit()
    return jsonify({"msg": "댓글이 수정되었습니다"}), 200

@bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get_or_404(comment_id)
    
    # 작성자 확인
    if comment.user_id != user_id:
        return jsonify({"msg": "권한이 없습니다"}), 403
    
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"msg": "댓글이 삭제되었습니다"}), 200