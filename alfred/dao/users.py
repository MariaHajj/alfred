from alfred.models import User
from alfred import db


class UserDAO():
    """Class to handle all database operations
    for models.User class.
    """
    __instance__ = None

    def __init__(self):
        if UserDAO.__instance__ is None:
            UserDAO.__instance__ = self
        else:
            raise Exception("You cannot create another UserDAO class")

    @staticmethod
    def get_instance():
        if not UserDAO.__instance__:
            UserDAO()
        return UserDAO.__instance__

    def add(self, user):
        db.session.add(user)
        db.session.commit()

    def get_all(self):
        return db.session.query(User).all()

    def get_by_id(self, user_id):
        return db.session.query(User).get(user_id)

    def get_by_aub_id(self, aub_id):
        return db.session.query(User).filter_by(aub_id=aub_id).first()

    def get_by_first_name(self, first_name):
        return db.session.query(User).filter_by(first_name=first_name).first()

    def get_by_last_name(self, last_name):
        return db.session.query(User).filter_by(last_name=last_name).first()

    def get_by_major(self, major):
        return db.session.query(User).filter_by(major=major).first()

    def get_by_email(self, email):
        return db.session.query(User).filter_by(email=email).first()

    def delete_user_by_id(self, user_id):
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()


user_dao = UserDAO.get_instance()
