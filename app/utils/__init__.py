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
                current_user = UserModel.query.get_or_404(get_jwt_identity(), description="User not found")

                if not current_user.is_admin():
                    abort(403, description="Forbidden")

            return fn(*args, **kwargs)

        return decorator

    return wrapper
