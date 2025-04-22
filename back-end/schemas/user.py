from extensions import ma
from models.user import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    user_id = ma.auto_field()
    pw = ma.auto_field(load_only=True)
    email = ma.auto_field()
    nickname = ma.auto_field()
