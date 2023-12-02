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
    return CategoryModel.query.all()


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


@blp.route("/<category_id>", methods=["GET"])
@blp.response(200, schema=CategorySchema)
@custom_jwt_required()
def get_category(category_id):
    return CategoryModel.query.get_or_404(category_id, description="Category not found")


@blp.route("/<category_id>", methods=["PUT", "PATCH"])
@blp.arguments(CategorySchema, as_kwargs=True)  # don't try to remove 'as_kwargs'
@blp.response(200, schema=CategorySchema)
@custom_jwt_required(is_admin=True)
def update_category(category_id, **category_data):
    category = CategoryModel.query.get_or_404(category_id, description="Category not found")

    for key, value in category_data.items():
        setattr(category, key, value)

    db.session.commit()
    return category


@blp.route("/<category_id>", methods=["DELETE"])
@blp.response(204)
@custom_jwt_required(is_admin=True)
def delete_category(category_id):
    category = CategoryModel.query.get_or_404(category_id, description="Category not found")

    db.session.delete(category)
    db.session.commit()
