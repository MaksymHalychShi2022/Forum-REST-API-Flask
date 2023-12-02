from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from app.db import db
from app.models.category import CategoryModel
from app.models.topic import TopicModel
from app.utils import custom_jwt_required
from schemas import TopicSchema, TopicContextSchema

blp = Blueprint("Topics", __name__, url_prefix="/topics")


@blp.route("", methods=["GET"])
@blp.arguments(TopicContextSchema)
@blp.response(200, schema=TopicSchema(many=True))
@custom_jwt_required()
def get_topics(topic_context):
    category = CategoryModel.query.get_or_404(topic_context["category_id"], description="Category not found")
    return category.topics


@blp.route("", methods=["POST"])
@blp.arguments(TopicSchema)
@blp.response(201, schema=TopicSchema)
@custom_jwt_required(is_admin=True)
def create_topic(topic_data):
    category = CategoryModel.query.get_or_404(topic_data["category_id"], description="Category not found")

    new_topic = TopicModel(
        title=topic_data["title"],
        body=topic_data["body"],
        category=category,
        user_id=get_jwt_identity()
    )

    db.session.add(new_topic)
    db.session.commit()

    return new_topic
