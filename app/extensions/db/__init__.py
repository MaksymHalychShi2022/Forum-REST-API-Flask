from flask_migrate import Migrate

from .setup import create_admin_user
from app.extensions.database import db

migrate = Migrate()


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)

    create_admin_user(app)
