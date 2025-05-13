from marshmallow import fields, validate
from extensions import ma
from models import User, BulletinBoard, Comment
import uuid

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
    
    # 관계 필드
    user = fields.Nested('UserSchema', only=('user_id', 'nickname'))
    post = fields.Nested('BulletinBoardSchema', exclude=('comments', 'user'))
    replies = fields.List(fields.Nested(lambda: CommentSchema(exclude=('replies', 'post'))))
    
    # API 응답 필드 이름 변경 (parent_com_id → pre_comid)
    pre_comid = fields.String(attribute='parent_com_id')

# 댓글 생성 스키마
class CommentCreateSchema(ma.Schema):
    content = fields.String(required=True, validate=validate.Length(min=1))
    pre_comid = fields.String(load_default=None)  # 부모 댓글 ID (대댓글인 경우)
    
    @staticmethod
    def generate_com_id():
        return f"C{uuid.uuid4().hex[:7].upper()}"

# 댓글 수정 스키마
class CommentUpdateSchema(ma.Schema):
    content = fields.String(required=True, validate=validate.Length(min=1))

# 댓글 목록 응답용 스키마 
class CommentListSchema(ma.Schema):
    com_id = fields.String()
    content = fields.String()
    nickname = fields.String(attribute='author.nickname')
    created_at = fields.DateTime()
    pre_comid = fields.String(attribute='parent_com_id')
    replies = fields.List(fields.Nested(lambda: CommentListSchema()))

# 인스턴스 생성
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
comment_create_schema = CommentCreateSchema()
comment_update_schema = CommentUpdateSchema()
comment_list_schema = CommentListSchema(many=True)