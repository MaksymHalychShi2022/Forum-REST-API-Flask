from marshmallow import Schema, fields

from app.schemas.auth import UserSchema


class CommentContextSchema(Schema):
    topic_id = fields.String(required=True)


class CommentSchema(Schema):
    id = fields.String(dump_only=True)
    body = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema)


class CommentWithContextSchema(CommentSchema, CommentContextSchema):
    pass
