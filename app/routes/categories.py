from flask import abort
from flask_smorest import Blueprint

from app.db import db
from app.models.category import CategoryModel
from app.utils import custom_jwt_required
from schemas import CategorySchema

blp = Blueprint("Categories", __name__, url_prefix="/categories")


@blp.route("", methods=["GET"])
@blp.response(200, schema=CategorySchema(many=True))
@custom_jwt_required()
def get_categories():
    categories = CategoryModel.query.all()
    return categories


@blp.route("", methods=["POST"])
@blp.arguments(CategorySchema)
@blp.response(201, schema=CategorySchema)
@custom_jwt_required(is_admin=True)
def create_category(category_data):
    existing_category = CategoryModel.query.filter_by(title=category_data['title']).first()
    if existing_category:
        abort(400, description=f"A category with the name '{category_data['title']}' already exists.")

    new_category = CategoryModel(**category_data)
    db.session.add(new_category)
    db.session.commit()
    return new_category
