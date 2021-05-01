from alfred.models import Major
from alfred import db


class MajorDAO():
    """Class to handle all database operations
    for models.Major class.
    """
    __instance__ = None

    def __init__(self):
        if MajorDAO.__instance__ is None:
            MajorDAO.__instance__ = self
        else:
            raise Exception("You cannot create another MajorDAO class")

    @staticmethod
    def get_instance():
        if not MajorDAO.__instance__:
            MajorDAO()
        return MajorDAO.__instance__

    def add(self, major):
        db.session.add(major)
        db.session.commit()

    def get_all(self):
        return db.session.query(Major).all()

    def get_by_id(self, major_id):
        return db.session.query(Major).get(major_id)

    def get_by_name(self, name):
        return db.session.query(Major).filter_by(name=name).first()

    def get_by_code(self, code):
        return db.session.query(Major).filter_by(code=code).first()

    def delete_major_by_id(self, major_id):
        db.session.query(Major).filter_by(id=major_id).delete()
        db.session.commit()


major_dao = MajorDAO.get_instance()
