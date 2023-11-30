from passlib.handlers.pbkdf2 import pbkdf2_sha256


def verify_password(password, correct_password):
    return pbkdf2_sha256.verify(password, correct_password)


def make_hash(password):
    return pbkdf2_sha256.hash(password)
