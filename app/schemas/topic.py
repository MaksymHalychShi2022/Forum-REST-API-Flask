from marshmallow import Schema, fields

from app.schemas.auth import UserSchema


class TopicContextSchema(Schema):
    category_id = fields.String(required=True)


class TopicSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    body = fields.String(required=True)
    closed = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema)
    # user_id = fields.String(dump_only=True)


class TopicWithContextSchema(TopicSchema, TopicContextSchema):
    pass
