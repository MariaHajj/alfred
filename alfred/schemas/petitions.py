from alfred.schemas import BaseSchema
from marshmallow import fields


class PetitionSchema(BaseSchema):
    __envelope__ = {"single": "petition", "many": "petitions"}

    class Meta:
        ordered = True

    transcript = fields.String(required=True)
    request_comment = fields.String(required=True)
    date_submitted = fields.Date(required=True)
    advisor_comment = fields.String(required=True)
    decision_comment = fields.String(required=True)
    date_decided = fields.Date(required=True)
