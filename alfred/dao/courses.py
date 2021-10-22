from alfred.models import Course
from alfred import db


class CourseDAO():
    """Class to handle all database operations
    for models.Course class.
    """
    __instance__ = None

    def __init__(self):
        if CourseDAO.__instance__ is None:
            CourseDAO.__instance__ = self
        else:
            raise Exception("You cannot create another CourseDAO class")

    @staticmethod
    def get_instance():
        if not CourseDAO.__instance__:
            CourseDAO()
        return CourseDAO.__instance__

    def add(self, course):
        db.session.add(course)
        db.session.commit()

    def get_all(self):
        return db.session.query(Course).all()

    def get_by_id(self, department_id):
        return db.session.query(Course).get(department_id)

    def get_by_name(self, name):
        return db.session.query(Course).filter_by(name=name).first()

    def get_by_code(self, code):
        return db.session.query(Course).filter_by(code=code).first()

    def get_by_number(self, number):
        return db.session.query(Course).filter_by(number=number).first()

    def delete_course_by_id(self, course_id):
        db.session.query(Course).filter_by(id=course_id).delete()
        db.session.commit()


course_dao = CourseDAO.get_instance()
