from alfred.schemas import BaseSchema
from marshmallow import fields


class PetitionStatusSchema(BaseSchema):
    __envelope__ = {"single": "status", "many": "statuses"}

    class Meta:
        ordered = True

    name = fields.String(required=True)
    description = fields.String(required=True)
