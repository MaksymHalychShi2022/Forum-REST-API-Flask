from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint
from flask import request

from app.extensions.database import db
from app.extensions.jwt.decorators import custom_jwt_required
from app.models.category import CategoryModel
from app.models.topic import TopicModel
from app.schemas.topic import TopicSchema, TopicContextSchema, TopicWithContextSchema

blp = Blueprint("Topics", __name__, url_prefix="/topics")


@blp.route("", methods=["GET"])
# @blp.arguments(TopicContextSchema)
@blp.response(200, schema=TopicSchema(many=True))
# @custom_jwt_required()
def get_topics():
    category_id = request.args.get('category_id')
    category = CategoryModel.query.get_or_404(category_id, description="Category not found")
    return category.topics


@blp.route("", methods=["POST"])
@blp.arguments(TopicWithContextSchema)
@blp.response(201, schema=TopicWithContextSchema)
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


@blp.route("/<topic_id>", methods=["GET"])
@blp.response(200, schema=TopicWithContextSchema)
@custom_jwt_required()
def get_topic(topic_id):
    return TopicModel.query.get_or_404(topic_id, description="Topic not found")


@blp.route("/<topic_id>", methods=["PUT", "PATCH"])
@blp.arguments(TopicSchema, as_kwargs=True)
@blp.response(200, schema=TopicWithContextSchema)
@custom_jwt_required(is_admin=True)
def update_topic(topic_id, **topic_data):
    topic = TopicModel.query.get_or_404(topic_id, description="Topic not found")

    for key, value in topic_data.items():
        setattr(topic, key, value)

    db.session.commit()
    return topic


@blp.route("/<topic_id>", methods=["DELETE"])
@blp.response(204)
@custom_jwt_required(is_admin=True)
def delete_topic(topic_id):
    topic = TopicModel.query.get_or_404(topic_id, description="Topic not found")

    db.session.delete(topic)
    db.session.commit()
