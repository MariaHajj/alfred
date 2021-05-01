from alfred.models import PetitionType
from alfred import db


class PetitionTypeDAO():
    """Class to handle all database operations
    for models.PetitionType class.
    """
    __instance__ = None

    def __init__(self):
        if PetitionTypeDAO.__instance__ is None:
            PetitionTypeDAO.__instance__ = self
        else:
            raise Exception("You cannot create another PetitionTypeDAO class")

    @staticmethod
    def get_instance():
        if not PetitionTypeDAO.__instance__:
            PetitionTypeDAO()
        return PetitionTypeDAO.__instance__

    def add(self, petition_type):
        db.session.add(petition_type)
        db.session.commit()

    def get_all(self):
        return db.session.query(PetitionType).all()

    def get_by_id(self, petition_type_id):
        return db.session.query(PetitionType).get(petition_type_id)

    def get_by_name(self, name):
        return db.session.query(PetitionType).filter_by(name=name).first()

    def delete_petition_type_by_id(self, petition_type_id):
        db.session.query(PetitionType).filter_by(id=petition_type_id).delete()
        db.session.commit()


petition_type_dao = PetitionTypeDAO.get_instance()
