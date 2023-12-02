from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models.role import RoleModel
from .models.user import UserModel
from .routes import auth_blueprint, categories_blueprint, topics_blueprint, comments_blueprint
from .db import db
from config import DevelopmentConfig
from .utils.utils import make_hash


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    create_admin_user(app)
    config_jwt(app)
    config_error_handlers(app)

    api.register_blueprint(auth_blueprint)
    api.register_blueprint(categories_blueprint)
    api.register_blueprint(topics_blueprint)
    api.register_blueprint(comments_blueprint)

    return app


def create_admin_user(app):
    with app.app_context():
        db.create_all()  # create tables
        if UserModel.query.filter_by(email="admin@exmple.com").first():
            return

        admin_role = create_admin_role()

        hashed_password = make_hash("password")
        new_user = UserModel(email="admin@exmple.com", username="admin", password=hashed_password)

        new_user.roles.append(admin_role)

        db.session.add(new_user)
        db.session.commit()


def create_admin_role():
    admin_role = RoleModel.query.filter_by(name='Admin').first()
    if not admin_role:
        admin_role = RoleModel(name='Admin')
        db.session.add(admin_role)
        db.session.commit()
    return admin_role


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
