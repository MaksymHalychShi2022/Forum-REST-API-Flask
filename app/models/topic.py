import uuid
from datetime import datetime

from app.db import db


class TopicModel(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    closed = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id', ondelete='CASCADE'))

    user = db.relationship("UserModel", backref="topics")
    category = db.relationship("CategoryModel", backref="topics")
