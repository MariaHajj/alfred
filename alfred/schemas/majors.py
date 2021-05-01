from alfred.schemas import BaseSchema
from marshmallow import fields


class MajorSchema(BaseSchema):
    __envelope__ = {"single": "major", "many": "majors"}

    class Meta:
        ordered = True

    name = fields.String(required=True)
    code = fields.String(required=True)
