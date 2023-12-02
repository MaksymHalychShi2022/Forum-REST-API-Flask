from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from app.db import db
from app.models.comment import CommentModel
from app.utils import custom_jwt_required
from schemas import CommentSchema

blp = Blueprint("Comments", __name__, url_prefix="/comments")


@blp.route("", methods=["GET"])
@blp.response(200, schema=CommentSchema(many=True))
@custom_jwt_required()
def get_comments():
    return CommentModel.query.all()


@blp.route("", methods=["POST"])
@blp.arguments(CommentSchema)
@blp.response(201, schema=CommentSchema)
@custom_jwt_required()
def create_comment(comment_data):
    new_comment = CommentModel(**comment_data)
    new_comment.user_id = get_jwt_identity()
    db.session.add(new_comment)
    db.session.commit()

    return new_comment
