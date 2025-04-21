from extensions import db

class User(db.Model):
    user_id = db.Column(db.String(50), primary_key=True)
    pw = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)

    boards = db.relationship('BulletinBoard', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
