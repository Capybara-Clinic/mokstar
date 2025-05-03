from extensions import ma
from models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('pw',)  # 비밀번호는 응답에서 제외

user_schema = UserSchema()
users_schema = UserSchema(many=True)