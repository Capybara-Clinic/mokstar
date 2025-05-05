from extensions import db

class Board(db.Model):
    __tablename__ = 'boards'

    board_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    view_cnt = db.Column(db.Integer, default=0)

    # 관계 설정
    user = db.relationship('User', backref='boards', lazy=True)

    def __repr__(self):
        return f"<Board {self.board_id}, {self.title}>"