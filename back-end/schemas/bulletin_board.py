from marshmallow import fields, validate
from extensions import ma
from models import User, BulletinBoard, Comment
import uuid

class BulletinBoardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BulletinBoard
        load_instance = True
        exclude = ('view_count',)  # view_count 필드 자동 생성에서 제외
    
    # 관계 필드
    user = fields.Nested('UserSchema', only=('user_id', 'nickname'))
    comments = fields.List(fields.Nested('CommentSchema', exclude=('post',)))
    
    # 커스텀 필드 - view_count를 view_cnt로 변환
    view_cnt = fields.Int(attribute='view_count')

# 게시글 생성 스키마
class BulletinBoardCreateSchema(ma.Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    content = fields.String(required=True)
    
    @staticmethod
    def generate_bill_id():
        return f"B{uuid.uuid4().hex[:7].upper()}"

# 게시글 수정 스키마
class BulletinBoardUpdateSchema(ma.Schema):
    title = fields.String(validate=validate.Length(min=1, max=255))
    content = fields.String()

# 게시글 목록 응답용 스키마
class BulletinBoardListSchema(ma.Schema):
    bill_id = fields.String()
    title = fields.String()
    nickname = fields.String(attribute='author.nickname')
    view_cnt = fields.Int(attribute='view_count')
    created_at = fields.DateTime()

# 인스턴스 생성
bulletin_board_schema = BulletinBoardSchema()
bulletin_boards_schema = BulletinBoardSchema(many=True)
bulletin_board_create_schema = BulletinBoardCreateSchema()
bulletin_board_update_schema = BulletinBoardUpdateSchema()
bulletin_board_list_schema = BulletinBoardListSchema(many=True)