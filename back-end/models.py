# models.py
from extensions import db
import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    nickname = db.Column(db.String(255), nullable=False, unique=True)
    
    # 관계 설정
    posts = db.relationship('BulletinBoard', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', nickname='{self.nickname}')>"


class BulletinBoard(db.Model):
    __tablename__ = 'bulletin_boards'
    
    bill_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 관계 설정
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<BulletinBoard(bill_id='{self.bill_id}', title='{self.title}')>"


class Comment(db.Model):
    __tablename__ = 'comments'
    
    com_id = db.Column(db.String(255), primary_key=True)
    bill_id = db.Column(db.String(255), db.ForeignKey('bulletin_boards.bill_id'), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    parent_com_id = db.Column(db.String(255), db.ForeignKey('comments.com_id'), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 대댓글 관계
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[com_id]), lazy=True)

    def __repr__(self):
        return f"<Comment(com_id='{self.com_id}', content='{self.content[:20]}...')>"