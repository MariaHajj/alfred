from alfred.schemas import BaseSchema
from marshmallow import fields


class FrequencySchema(BaseSchema):
    __envelope__ = {"single": "frequency", "many": "frequencies"}

    class Meta:
        ordered = True

    value = fields.String(required=True)
    description = fields.String(required=True)
