from flask_jwt_extended import JWTManager

from .setup import set_jwt_callbacks

jwt = JWTManager()


def init_app(app):
    jwt.init_app(app)
    set_jwt_callbacks(jwt)
