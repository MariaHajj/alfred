from alfred.schemas import BaseSchema
from marshmallow import fields


class CourseSchema(BaseSchema):
    __envelope__ = {"single": "course", "many": "courses"}

    class Meta:
        ordered = True

    name = fields.String(required=True)
    description = fields.String(required=True)
    code = fields.String(required=True)
    number = fields.Integer(required=True)
