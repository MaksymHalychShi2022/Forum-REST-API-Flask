from marshmallow import Schema, fields


class CommentContextSchema(Schema):
    topic_id = fields.String(required=True)


class CommentSchema(Schema):
    id = fields.String(dump_only=True)
    body = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.String(dump_only=True)


class CommentWithContextSchema(CommentSchema, CommentContextSchema):
    pass
