from marshmallow import fields, validate, validates, ValidationError
from extensions import ma
from models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)  # 응답에 비밀번호 포함하지 않음
    
    # 관계
    posts = fields.List(fields.Nested('BulletinBoardSchema', exclude=('user', 'comments')))

# 회원가입 요청 스키마
class UserRegisterSchema(ma.Schema):
    user_id = fields.String(required=True, validate=validate.Length(min=4, max=20))
    email = fields.Email(required=True)
    nickname = fields.String(required=True, validate=validate.Length(min=2, max=20))
    pw = fields.String(required=True, validate=validate.Length(min=8))
    
    # 수정된 유효성 검사 메서드들
    @validates('user_id')
    def validate_user_id(self, value, **kwargs):  # kwargs 추가
        if User.query.filter_by(user_id=value).first():
            raise ValidationError('이미 사용 중인 아이디입니다.')
    
    @validates('email')
    def validate_email(self, value, **kwargs):  # kwargs 추가
        if User.query.filter_by(email=value).first():
            raise ValidationError('이미 사용 중인 이메일입니다.')
    
    @validates('nickname')
    def validate_nickname(self, value, **kwargs):  # kwargs 추가
        if User.query.filter_by(nickname=value).first():
            raise ValidationError('이미 사용 중인 닉네임입니다.')

# 로그인 요청 스키마
class UserLoginSchema(ma.Schema):
    user_id = fields.String(required=True)
    pw = fields.String(required=True)

# 로그인/회원가입 응답 스키마
class AuthResponseSchema(ma.Schema):
    access_token = fields.String()
    user = fields.Nested(lambda: UserSchema(only=('user_id', 'nickname')))

# 인스턴스 생성
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
auth_response_schema = AuthResponseSchema()