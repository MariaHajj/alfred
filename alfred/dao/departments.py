from alfred.models import Department
from alfred import db


class DepartmentDAO():
    """Class to handle all database operations
    for models.Department class.
    """
    __instance__ = None

    def __init__(self):
        if DepartmentDAO.__instance__ is None:
            DepartmentDAO.__instance__ = self
        else:
            raise Exception("You cannot create another DepartmentDAO class")

    @staticmethod
    def get_instance():
        if not DepartmentDAO.__instance__:
            DepartmentDAO()
        return DepartmentDAO.__instance__

    def add(self, department):
        db.session.add(department)
        db.session.commit()

    def get_all(self):
        return db.session.query(Department).all()

    def get_by_id(self, department_id):
        return db.session.query(Department).get(department_id)

    def get_by_name(self, name):
        return db.session.query(Department).filter_by(name=name).first()

    def get_by_code(self, code):
        return db.session.query(Department).filter_by(code=code).first()

    def delete_department_by_id(self, department_id):
        db.session.query(Department).filter_by(id=department_id).delete()
        db.session.commit()


department_dao = DepartmentDAO.get_instance()
