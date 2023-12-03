import uuid

from app.extensions.database import db

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.String(36), db.ForeignKey('roles.id', ondelete='RESTRICT'), primary_key=True)
)


class RoleModel(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    users = db.relationship('UserModel', secondary=user_roles, back_populates='roles')
