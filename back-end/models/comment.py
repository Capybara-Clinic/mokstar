from extensions import db

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.board_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # 관계 설정
    user = db.relationship('User', backref='comments', lazy=True)
    board = db.relationship('Board', backref='comments', lazy=True)

    def __repr__(self):
        return f"<Comment {self.comment_id}, {self.content[:20]}>"