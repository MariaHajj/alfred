from alfred.schemas import BaseSchema
from marshmallow import fields


class FacultySchema(BaseSchema):
    __envelope__ = {"single": "faculty", "many": "faculties"}

    class Meta:
        ordered = True

    name = fields.String(required=True)
    code = fields.String(required=True)
