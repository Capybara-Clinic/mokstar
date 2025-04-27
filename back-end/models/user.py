from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(255), primary_key=True, comment='중복 허용 안함')
    pw = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, comment='중복 허용 안함')
    nickname = db.Column(db.String(255), unique=True, nullable=False, comment='중복 허용 안함')

    # 관계 설정 (optional)
    boards = db.relationship('Board', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)