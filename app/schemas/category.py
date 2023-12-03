from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
