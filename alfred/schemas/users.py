from alfred.schemas import BaseSchema
from marshmallow import fields


class UserSchema(BaseSchema):
    __envelope__ = {"single": "user", "many": "users"}

    class Meta:
        ordered = True

    aub_id = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    major = fields.String(required=True)
    password = fields.String(required=True)
    image_file = fields.String(required=True)
