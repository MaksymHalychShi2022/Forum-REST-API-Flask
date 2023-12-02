from flask_smorest import Blueprint

from app.db import db
from app.models.topic import TopicModel
from app.utils import custom_jwt_required
from schemas import TopicSchema

blp = Blueprint("Topics", __name__, url_prefix="/topics")


@blp.route("", methods=["GET"])
@blp.response(200, schema=TopicSchema(many=True))
@custom_jwt_required()
def get_topics():
    return TopicModel.query.all()


@blp.route("", methods=["POST"])
@blp.arguments(TopicSchema)
@blp.response(201, schema=TopicSchema)
@custom_jwt_required(is_admin=True)
def create_topic(topic_data):
    new_topic = TopicModel(**topic_data)

    db.session.add(new_topic)
    db.session.commit()

    return new_topic
