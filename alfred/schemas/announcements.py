from alfred.schemas import BaseSchema
from marshmallow import fields


class AnnouncementSchema(BaseSchema):
    __envelope__ = {"single": "announcement", "many": "announcements"}

    class Meta:
        ordered = True

    title = fields.String(required=True)
    description = fields.String(required=True)
