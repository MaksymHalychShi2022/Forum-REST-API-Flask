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


class RoleSchema(Schema):
    # id = fields.String(dump_only=True)
    name = fields.String()


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    username = fields.String()
    description = fields.String()


class UserWithRolesSchema(UserSchema):
    roles = fields.Nested(RoleSchema, many=True, dump_only=True)
