from flask_testing import TestCase

from alfred import create_app, db
from alfred.config import TestConfig
from alfred.models import User


class BaseTestCase(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()
        db.session.add(
            User(username="admin", email="ad@min.com", password="admin")
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
