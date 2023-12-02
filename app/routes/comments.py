from flask import abort
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from app.db import db
from app.models.comment import CommentModel
from app.models.topic import TopicModel
from app.utils import custom_jwt_required
from schemas import CommentSchema, CommentContextSchema

blp = Blueprint("Comments", __name__, url_prefix="/comments")


@blp.route("", methods=["GET"])
@blp.arguments(CommentContextSchema)
@blp.response(200, schema=CommentSchema(many=True))
@custom_jwt_required()
def get_comments(comment_context):
    topic = TopicModel.query.get_or_404(comment_context["topic_id"], description="Topic not found")
    return topic.comments


@blp.route("", methods=["POST"])
@blp.arguments(CommentSchema)
@blp.response(201, schema=CommentSchema)
@custom_jwt_required()
def create_comment(comment_data):
    topic = TopicModel.query.get_or_404(comment_data["topic_id"], description="Topic not found")

    if topic.closed:
        abort(400, description="Topic is closed")

    new_comment = CommentModel(body=comment_data["body"])
    new_comment.topic = topic
    new_comment.user_id = get_jwt_identity()

    db.session.add(new_comment)
    db.session.commit()

    return new_comment
