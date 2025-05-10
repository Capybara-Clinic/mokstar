from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, BulletinBoard, Comment
from schemas.comment import (
    comment_schema, comments_schema, 
    comment_create_schema, comment_update_schema,
    comment_list_schema
)

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/board/<string:bill_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(bill_id):
    """댓글 작성"""
    user_id = get_jwt_identity()
    
    # 게시글 확인
    post = BulletinBoard.query.filter_by(bill_id=bill_id).first()
    if not post:
        return jsonify(message="게시글을 찾을 수 없습니다"), 404
    
    # 사용자 확인
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify(message="사용자를 찾을 수 없습니다"), 404
    
    # 요청 데이터 검증
    json_data = request.get_json()
    if not json_data:
        return jsonify(message="데이터가 제공되지 않았습니다"), 400
    
    # 유효성 검사
    errors = comment_create_schema.validate(json_data)
    if errors:
        return jsonify(errors=errors), 400
    
    # 부모 댓글 ID 처리 (대댓글인 경우)
    parent_com_id = json_data.get('pre_comid')
    if parent_com_id:
        parent_comment = Comment.query.filter_by(com_id=parent_com_id).first()
        if not parent_comment:
            return jsonify(message="부모 댓글을 찾을 수 없습니다"), 404
    
    try:
        # 댓글 ID 생성
        com_id = comment_create_schema.generate_com_id()
        
        # 댓글 생성
        comment = Comment(
            com_id=com_id,
            bill_id=bill_id,
            user_id=user_id,
            content=json_data['content'],
            parent_com_id=parent_com_id
        )
        
        # DB에 저장
        db.session.add(comment)
        db.session.commit()
        
        return comment_schema.dump(comment), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message=str(e)), 500

@comment_bp.route('/board/<string:bill_id>/comments', methods=['GET'])
def get_comments(bill_id):
    """댓글 목록 조회"""
    # 게시글 확인
    post = BulletinBoard.query.filter_by(bill_id=bill_id).first()
    if not post:
        return jsonify(message="게시글을 찾을 수 없습니다"), 404
    
    # 최상위 댓글만 조회 (parent_com_id가 NULL인 댓글)
    comments = Comment.query.filter_by(bill_id=bill_id, parent_com_id=None).order_by(Comment.created_at).all()
    
    # 응답 데이터
    result = comment_list_schema.dump(comments)
    
    return jsonify(result), 200

@comment_bp.route('/comments/<string:com_id>', methods=['PUT'])
@jwt_required()
def update_comment(com_id):
    """댓글 수정"""
    user_id = get_jwt_identity()
    
    # 댓글 조회
    comment = Comment.query.filter_by(com_id=com_id).first()
    if not comment:
        return jsonify(message="댓글을 찾을 수 없습니다"), 404
    
    # 권한 확인
    if comment.user_id != user_id:
        return jsonify(message="댓글을 수정할 권한이 없습니다"), 403
    
    # 요청 데이터 검증
    json_data = request.get_json()
    if not json_data:
        return jsonify(message="데이터가 제공되지 않았습니다"), 400
    
    # 유효성 검사
    errors = comment_update_schema.validate(json_data)
    if errors:
        return jsonify(errors=errors), 400
    
    try:
        # 댓글 내용 업데이트
        comment.content = json_data['content']
        
        # DB 저장
        db.session.commit()
        
        return comment_schema.dump(comment), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message=str(e)), 500

@comment_bp.route('/comments/<string:com_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(com_id):
    """댓글 삭제"""
    user_id = get_jwt_identity()
    
    # 댓글 조회
    comment = Comment.query.filter_by(com_id=com_id).first()
    if not comment:
        return jsonify(message="댓글을 찾을 수 없습니다"), 404
    
    # 권한 확인
    if comment.user_id != user_id:
        return jsonify(message="댓글을 삭제할 권한이 없습니다"), 403
    
    try:
        # DB에서 댓글 삭제
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify(message="댓글이 삭제되었습니다"), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message=str(e)), 500