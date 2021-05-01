from alfred.schemas import BaseSchema
from marshmallow import fields


class PetitionSchema(BaseSchema):
    __envelope__ = {"single": "petition", "many": "petitions"}

    class Meta:
        ordered = True

    transcript = fields.String(required=True)
    request_comment = fields.String(required=True)
    date_submitted = fields.DateTime(required=True)
    petition_type = fields.String(required=True)
    course = fields.String(required=True)
    petition_status = fields.String(required=True)
    advisor_comment = fields.String(required=False)
    decision_comment = fields.String(required=False)
    date_decided = fields.Date(required=False)
    user = fields.String(required=True)
