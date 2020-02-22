from werkzeug.security import generate_password_hash, check_password_hash


def generate_hash(password):
    return generate_password_hash(password, method="pbkdf2:sha1")


def check_hash(pwhash, pw):
    return check_password_hash(pwhash, pw)
