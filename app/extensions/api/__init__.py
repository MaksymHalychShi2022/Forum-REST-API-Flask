from flask_smorest import Api
from app.routes import auth_blueprint, categories_blueprint, topics_blueprint, comments_blueprint

api = Api()


def init_app(app):
    api.init_app(app)

    api.register_blueprint(auth_blueprint)
    api.register_blueprint(categories_blueprint)
    api.register_blueprint(topics_blueprint)
    api.register_blueprint(comments_blueprint)
