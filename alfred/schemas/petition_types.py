from alfred.schemas import BaseSchema
from marshmallow import fields


class PetitionTypeSchema(BaseSchema):
    __envelope__ = {"single": "type", "many": "types"}

    class Meta:
        ordered = True

    name = fields.String(required=True)
    description = fields.String(required=True)
