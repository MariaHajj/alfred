from alfred.models import PetitionStatus
from alfred import db


class PetitionStatusDAO():
    """Class to handle all database operations
    for models.PetitionStatus class.
    """
    __instance__ = None

    def __init__(self):
        if PetitionStatusDAO.__instance__ is None:
            PetitionStatusDAO.__instance__ = self
        else:
            raise Exception("You cannot create another"
                            "PetitionStatusDAO class")

    @staticmethod
    def get_instance():
        if not PetitionStatusDAO.__instance__:
            PetitionStatusDAO()
        return PetitionStatusDAO.__instance__

    def add(self, petition_status):
        db.session.add(petition_status)
        db.session.commit()

    def get_all(self):
        return db.session.query(PetitionStatus).all()

    def get_by_id(self, petition_status_id):
        return db.session.query(PetitionStatus).get(petition_status_id)

    def get_by_name(self, name):
        return db.session.query(PetitionStatus).filter_by(name=name).first()

    def delete_petition_status_by_id(self, petition_status_id):
        db.session.query(PetitionStatus)\
            .filter_by(id=petition_status_id).delete()
        db.session.commit()


petition_status_dao = PetitionStatusDAO.get_instance()
