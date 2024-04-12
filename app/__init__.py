from flask import Flask, jsonify
from flask_cors import CORS

from .extensions import jwt, db, api
from .extensions.config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    jwt.init_app(app)
    db.init_app(app)
    api.init_app(app)

    register_error_handlers(app)

    return app


def register_error_handlers(app):
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

    @app.errorhandler(403)
    def unauthorized(error):
        response = jsonify({"message": error.description})
        response.status_code = 403
        return response

    @app.errorhandler(404)
    def unauthorized(error):
        response = jsonify({"message": error.description})
        response.status_code = 404
        return response
