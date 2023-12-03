from flask import abort
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from app.db import db
from app.models.user import UserModel
from app.models.comment import CommentModel
from app.models.topic import TopicModel
from app.utils import custom_jwt_required
from schemas import CommentSchema, CommentContextSchema, CommentWithContextSchema

blp = Blueprint("Comments", __name__, url_prefix="/comments")


@blp.route("", methods=["GET"])
@blp.arguments(CommentContextSchema)
@blp.response(200, schema=CommentSchema(many=True))
@custom_jwt_required()
def get_comments(comment_context):
    topic = TopicModel.query.get_or_404(comment_context["topic_id"], description="Topic not found")
    return topic.comments


@blp.route("", methods=["POST"])
@blp.arguments(CommentWithContextSchema)
@blp.response(201, schema=CommentWithContextSchema)
@custom_jwt_required()
def create_comment(comment_data):
    topic = TopicModel.query.get_or_404(comment_data["topic_id"], description="Topic not found")

    if topic.closed:
        abort(400, description="Topic is closed")

    new_comment = CommentModel(
        body=comment_data["body"],
        topic=topic,
        user_id=get_jwt_identity()
    )

    db.session.add(new_comment)
    db.session.commit()

    return new_comment


@blp.route("/<comment_id>", methods=["GET"])
@blp.response(200, schema=CommentWithContextSchema)
@custom_jwt_required()
def get_comment(comment_id):
    return CommentModel.query.get_or_404(comment_id, description="Comment not found")


@blp.route("/<comment_id>", methods=["PUT", "PATCH"])
@blp.arguments(CommentSchema, as_kwargs=True)
@blp.response(200, schema=CommentWithContextSchema)
@custom_jwt_required()
def update_comment(comment_id, **comment_data):
    comment = CommentModel.query.get_or_404(comment_id, description="Comment not found")
    current_user = UserModel.query.get_or_404(get_jwt_identity(), description="User not found")

    if comment.user_id != current_user.id and not current_user.is_admin():
        abort(403, description="Forbidden")

    comment.body = comment_data["body"]
    db.session.commit()
    return comment


@blp.route("/<string:comment_id>", methods=["DELETE"])
@blp.response(204)
@custom_jwt_required()
def delete_comment(comment_id):
    comment = CommentModel.query.get_or_404(comment_id, description="Comment not found")
    current_user = UserModel.query.get_or_404(get_jwt_identity(), description="User not found")

    if comment.user_id != current_user.id and not current_user.is_admin():
        abort(403, description="Forbidden")

    db.session.delete(comment)
    db.session.commit()
