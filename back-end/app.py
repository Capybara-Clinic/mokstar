from flask import Flask
from extensions import db, ma, jwt
from config import Config

from routes.auth import auth_bp
from routes.board import board_bp
from routes.comment import comment_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(board_bp, url_prefix="/board")
    app.register_blueprint(comment_bp, url_prefix="/board")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
