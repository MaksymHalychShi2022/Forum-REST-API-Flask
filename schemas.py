from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=1))


class LoginResponseSchema(Schema):
    access_token = fields.String()


class RegisterSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email(error="Invalid email"))
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    username = fields.String()
    description = fields.String()


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()


class TopicSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    body = fields.String(required=True)
    closed = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.String()
    category_id = fields.String()
