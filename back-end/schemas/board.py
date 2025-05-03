from extensions import ma
from models.board import Board
from schemas.user import UserSchema
from marshmallow import fields

class BoardSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema(only=('user_id', 'nickname')))
    
    class Meta:
        model = Board
        include_fk = True

board_schema = BoardSchema()
boards_schema = BoardSchema(many=True)