from alfred.models import Faculty
from alfred import db


class FacultyDAO():
    """Class to handle all database operations
    for models.Faculty class.
    """
    __instance__ = None

    def __init__(self):
        if FacultyDAO.__instance__ is None:
            FacultyDAO.__instance__ = self
        else:
            raise Exception("You cannot create another FacultyDAO class")

    @staticmethod
    def get_instance():
        if not FacultyDAO.__instance__:
            FacultyDAO()
        return FacultyDAO.__instance__

    def add(self, faculty):
        db.session.add(faculty)
        db.session.commit()

    def get_all(self):
        return db.session.query(Faculty).all()

    def get_by_id(self, faculty_id):
        return db.session.query(Faculty).get(faculty_id)

    def get_by_name(self, name):
        return db.session.query(Faculty).filter_by(name=name).first()

    def get_by_code(self, code):
        return db.session.query(Faculty).filter_by(code=code).first()

    def delete_faculty_by_id(self, faculty_id):
        db.session.query(Faculty).filter_by(id=faculty_id).delete()
        db.session.commit()


faculty_dao = FacultyDAO.get_instance()
