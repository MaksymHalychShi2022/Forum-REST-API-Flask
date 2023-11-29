from flask import abort
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from db import db
from models.user import UserModel
from schemas import LoginSchema, LoginResponseSchema, RegisterSchema, UserSchema
from utils.utils import verify_password, make_hash

blp = Blueprint("Auth", __name__, url_prefix="/auth")


@blp.route("/login", methods=["POST"])
@blp.arguments(LoginSchema)
@blp.response(201, schema=LoginResponseSchema)
def login(login_data):
    user = UserModel.query.filter(UserModel.email == login_data["email"]).first()

    if not user or not verify_password(login_data["password"], user.password):
        abort(401, description="Invalid credentials")

    return {
        "access_token": create_access_token(identity=user.id)
    }


@blp.route("/register", methods=["POST"])
@blp.arguments(RegisterSchema)
@blp.response(201, schema=UserSchema)
def register(register_data):
    if UserModel.query.filter(UserModel.email == register_data["email"]).first():
        abort(400, description="User already exist")

    user = UserModel(
        email=register_data["email"],
        password=make_hash(register_data["password"]),
        username=register_data["username"]
    )
    db.session.add(user)
    db.session.commit()
    return user


@blp.route("/user", methods=["GET"])
@blp.response(200, schema=UserSchema)
@jwt_required()
def get_user():
    return UserModel.query.get_or_404(get_jwt_identity())


@blp.route("/user", methods=["PUT", "PATCH"])
@blp.arguments(UserSchema)
@blp.response(200, schema=UserSchema)
@jwt_required()
def update_user(user_data):
    user = UserModel.query.get_or_404(get_jwt_identity())
    for key, value in user_data.items():
        setattr(user, key, value)

    db.session.commit()

    return user
