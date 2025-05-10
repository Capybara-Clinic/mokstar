from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, BulletinBoard, Comment
from schemas.bulletin_board import (
    bulletin_board_schema, bulletin_boards_schema, 
    bulletin_board_create_schema, bulletin_board_update_schema,
    bulletin_board_list_schema
)
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

board_bp = Blueprint('board', __name__, url_prefix='/board')

# 파일 업로드 지원 함수
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 파일명 중복 방지를 위한 고유 ID 추가
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # 업로드 폴더가 없으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 파일 저장
        file.save(file_path)
        return os.path.join('uploads', unique_filename)
    return None

@board_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """게시글 작성"""
    user_id = get_jwt_identity()
    
    # 사용자 확인
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify(message="사용자를 찾을 수 없습니다"), 404
    
    # 폼 데이터에서 정보 추출
    title = request.form.get('title')
    content = request.form.get('content')
    
    # 유효성 검사
    data = {'title': title, 'content': content}
    errors = bulletin_board_create_schema.validate(data)
    if errors:
        return jsonify(errors=errors), 400
    
    # 파일 처리
    file_path = None
    if 'file' in request.files:
        file = request.files['file']
        file_path = save_file(file)
    
    try:
        # 게시글 ID 생성
        bill_id = bulletin_board_create_schema.generate_bill_id()
        
        # 게시글 생성
        post = BulletinBoard(
            bill_id=bill_id,
            user_id=user_id,
            title=title,
            content=content,
            file_path=file_path,
            view_count=0
        )
        
        # DB에 저장
        db.session.add(post)
        db.session.commit()
        
        return bulletin_board_schema.dump(post), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message=str(e)), 500

@board_bp.route('', methods=['GET'])
def get_posts():
    """게시글 목록 조회"""
    # 페이지네이션 파라미터
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 게시글 조회 (최신순)
    posts = BulletinBoard.query.order_by(BulletinBoard.created_at.desc()).paginate(page=page, per_page=per_page)
    
    # 응답 데이터
    result = bulletin_board_list_schema.dump(posts.items)
    
    return jsonify(result), 200

@board_bp.route('/<string:bill_id>', methods=['GET'])
def get_post(bill_id):
    """게시글 상세 조회"""
    # 게시글 조회
    post = BulletinBoard.query.filter_by(bill_id=bill_id).first()
    if not post:
        return jsonify(message="게시글을 찾을 수 없습니다"), 404
    
    # 조회수 증가
    post.view_count += 1
    db.session.commit()
    
    # 응답 데이터
    result = bulletin_board_schema.dump(post)
    
    return jsonify(result), 200

@board_bp.route('/<string:bill_id>', methods=['PUT'])
@jwt_required()
def update_post(bill_id):
    """게시글 수정"""
    user_id = get_jwt_identity()
    
    # 게시글 조회
    post = BulletinBoard.query.filter_by(bill_id=bill_id).first()
    if not post:
        return jsonify(message="게시글을 찾을 수 없습니다"), 404
    
    # 권한 확인
    if post.user_id != user_id:
        return jsonify(message="게시글을 수정할 권한이 없습니다"), 403
    
    # 요청 데이터 처리
    if request.content_type.startswith('application/json'):
        # JSON 요청
        json_data = request.get_json()
        errors = bulletin_board_update_schema.validate(json_data)
        if errors:
            return jsonify(errors=errors), 400
        
        # 필드 업데이트
        if 'title' in json_data:
            post.title = json_data['title']
        if 'content' in json_data:
            post.content = json_data['content']
            
    else:
        # 폼 데이터 요청
        title = request.form.get('title')
        content = request.form.get('content')
        
        # 유효성 검사
        data = {}
        if title:
            data['title'] = title
        if content:
            data['content'] = content
            
        errors = bulletin_board_update_schema.validate(data)
        if errors:
            return jsonify(errors=errors), 400
        
        # 필드 업데이트
        if title:
            post.title = title
        if content:
            post.content = content
            
        # 파일 처리
        if 'file' in request.files:
            file = request.files['file']
            if file:
                # 기존 파일 삭제
                if post.file_path:
                    old_file_path = os.path.join(current_app.root_path, post.file_path)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # 새 파일 저장
                file_path = save_file(file)
                if file_path:
                    post.file_path = file_path
    
    try:
        # 업데이트 시간 갱신
        post.updated_at = datetime.utcnow()
        
        # DB 저장
        db.session.commit()
        
        return bulletin_board_schema.dump(post), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message=str(e)), 500

@board_bp.route('/<string:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_post(bill_id):
    """게시글 삭제"""
    user_id = get_jwt_identity()
    
    # 게시글 조회
    post = BulletinBoard.query.filter_by(bill_id=bill_id).first()
    if not post:
        return jsonify(message="게시글을 찾을 수 없습니다"), 404
    
    # 권한 확인
    if post.user_id != user_id:
        return jsonify(message="게시글을 삭제할 권한이 없습니다"), 403
    
    try:
        # 파일 삭제
        if post.file_path:
            file_path = os.path.join(current_app.root_path, post.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # DB에서 게시글 삭제
        db.session.delete(post)
        db.session.commit()
        
        return jsonify(message="게시글이 삭제되었습니다"), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message=str(e)), 500