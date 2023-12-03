import uuid

from app.extensions.database import db
from app.models.role import user_roles


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    roles = db.relationship('RoleModel', secondary=user_roles, back_populates='users')

    def is_admin(self):
        return any(role.name == 'Admin' for role in self.roles)
