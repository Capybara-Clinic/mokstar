from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db, bcrypt
from models import User, BulletinBoard, Comment
from schemas.user import user_register_schema, user_login_schema, auth_response_schema
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """사용자 회원가입"""
    # 요청 데이터 검증
    json_data = request.get_json()
    if not json_data:
        return jsonify(message="데이터가 제공되지 않았습니다"), 400
        
    # 데이터 유효성 검사
    errors = user_register_schema.validate(json_data)
    if errors:
        return jsonify(errors=errors), 400
    
    # 사용자 객체 생성
    try:
        # 비밀번호 해싱
        hashed_pw = bcrypt.generate_password_hash(json_data['pw']).decode('utf-8')
        
        # 사용자 생성
        new_user = User(
            user_id=json_data['user_id'],
            password=hashed_pw,
            email=json_data['email'],
            nickname=json_data['nickname']
        )
        
        # DB에 저장
        db.session.add(new_user)
        db.session.commit()
        
        # JWT 토큰 생성
        access_token = create_access_token(identity=new_user.user_id)
        
        # 응답 데이터 생성
        response_data = {
            'access_token': access_token,
            'user': {
                'user_id': new_user.user_id,
                'nickname': new_user.nickname
            }
        }
        
        return auth_response_schema.dump(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message=str(e)), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """사용자 로그인"""
    # 요청 데이터 검증
    json_data = request.get_json()
    if not json_data:
        return jsonify(message="데이터가 제공되지 않았습니다"), 400
    
    # 데이터 유효성 검사
    errors = user_login_schema.validate(json_data)
    if errors:
        return jsonify(errors=errors), 400
    
    # 사용자 조회
    user = User.query.filter_by(user_id=json_data['user_id']).first()
    if not user or not bcrypt.check_password_hash(user.password, json_data['pw']):
        return jsonify(message="아이디 또는 비밀번호가 잘못되었습니다"), 401
    
    # JWT 토큰 생성
    access_token = create_access_token(identity=user.user_id)
    
    # 응답 데이터 생성
    response_data = {
        'access_token': access_token,
        'user': {
            'user_id': user.user_id,
            'nickname': user.nickname
        }
    }
    
    return auth_response_schema.dump(response_data), 200