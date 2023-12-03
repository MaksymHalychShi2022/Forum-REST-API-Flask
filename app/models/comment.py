import uuid
from datetime import datetime

from app.extensions.database import db


class CommentModel(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    topic_id = db.Column(db.String(36), db.ForeignKey('topics.id', ondelete='CASCADE'))

    user = db.relationship("UserModel", backref="comments")
    topic = db.relationship("TopicModel", backref="comments")
