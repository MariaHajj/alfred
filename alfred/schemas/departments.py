from alfred.schemas import BaseSchema
from marshmallow import fields


class DepartmentSchema(BaseSchema):
    __envelope__ = {"single": "department", "many": "departments"}

    class Meta:
        ordered = True

    name = fields.String(required=True)
    code = fields.String(required=True)
