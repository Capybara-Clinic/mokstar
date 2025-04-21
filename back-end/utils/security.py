from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(pw):
    return generate_password_hash(pw)

def verify_password(hashed_pw, input_pw):
    return check_password_hash(hashed_pw, input_pw)
