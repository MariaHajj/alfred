from alfred.models import Frequency
from alfred import db


class FrequencyDAO():
    """Class to handle all database operations
    for models.Frequency class.
    """
    __instance__ = None

    def __init__(self):
        if FrequencyDAO.__instance__ is None:
            FrequencyDAO.__instance__ = self
        else:
            raise Exception("You cannot create another FrequencyDAO class")

    @staticmethod
    def get_instance():
        if not FrequencyDAO.__instance__:
            FrequencyDAO()
        return FrequencyDAO.__instance__

    def add(self, frequency):
        db.session.add(frequency)
        db.session.commit()

    def get_all(self):
        return db.session.query(Frequency).all()

    def get_by_id(self, frequency_id):
        return db.session.query(Frequency).get(frequency_id)

    def get_by_value(self, value):
        return db.session.query(Frequency).filter_by(value=value).first()

    def delete_frequency_by_id(self, frequency_id):
        db.session.query(Frequency).filter_by(id=frequency_id).delete()
        db.session.commit()


frequency_dao = FrequencyDAO.get_instance()
