class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/moksta"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "your_secret_key"
    UPLOAD_FOLDER = "./media"
