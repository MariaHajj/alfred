from alfred.schemas import BaseSchema
from marshmallow import fields


class CapacitySurveySchema(BaseSchema):
    __envelope__ = {"single": "survey", "many": "surveys"}

    class Meta:
        ordered = True

    title = fields.String(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    number_of_requests = fields.Integer(required=False)
    comment = fields.String(required=True)
