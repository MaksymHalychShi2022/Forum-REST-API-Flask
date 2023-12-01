from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from app.models.user import UserModel


def custom_jwt_required(is_admin=False):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if is_admin:
                current_user_id = get_jwt_identity()
                current_user = UserModel.query.get(current_user_id)

                if not current_user:
                    abort(401)

                if not current_user.is_admin():
                    print(current_user.email)
                    print(current_user.roles)
                    abort(403)

            return fn(*args, **kwargs)

        return decorator

    return wrapper
