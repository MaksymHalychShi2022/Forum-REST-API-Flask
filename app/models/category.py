import uuid

from app.extensions.database import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    title = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(1000))
