from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .routes import auth_blueprint
from .db import db
from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    config_jwt(app)
    config_error_handlers(app)

    api.register_blueprint(auth_blueprint)

    return app


def config_jwt(app):
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback():
        response = jsonify({"message": "The token has expired"})
        response.status_code = 401
        return response

    @jwt.invalid_token_loader
    def invalid_token_callback():
        response = jsonify({"message": "Signature verification failed"})
        response.status_code = 401
        return response

    @jwt.unauthorized_loader
    def missing_token_callback():
        response = jsonify({"message": "Request does not contain an access token"})
        response.status_code = 401
        return response


def config_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({"message": error.description})
        response.status_code = 400
        return response

    @app.errorhandler(401)
    def unauthorized(error):
        response = jsonify({"message": error.description})
        response.status_code = 401
        return response
