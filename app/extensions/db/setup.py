from app.extensions.database import db
from app.models.role import RoleModel
from app.models.user import UserModel
from app.utils.auth import make_hash


def create_admin_user(app):
    with app.app_context():
        db.create_all()  # create tables
        if UserModel.query.filter_by(email="admin@example.com").first():
            return

        admin_role = create_admin_role()

        hashed_password = make_hash("password")
        new_user = UserModel(email="admin@example.com", username="admin", password=hashed_password)

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
