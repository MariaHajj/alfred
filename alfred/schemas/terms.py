from alfred.schemas import BaseSchema
from marshmallow import fields


class TermSchema(BaseSchema):
    __envelope__ = {"single": "term", "many": "terms"}

    class Meta:
        ordered = True

    name = fields.String(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
