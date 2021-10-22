from alfred.dao.courses import course_dao, Course, db


class CourseService():
    __instance__ = None

    def __init__(self):
        if CourseService.__instance__ is None:
            CourseService.__instance__ = self
        else:
            raise Exception("You cannot create another CourseService class")

    @staticmethod
    def get_instance():
        if not CourseService.__instance__:
            CourseService()
        return CourseService.__instance__

    def create_course(self, name, description, code, number):
        if (name is None) or (description is None)\
           or (code is None) or (number is None):
            return None

        course = course_dao.get_by_name(name=name)
        if course is None:
            course = Course(name=name, description=description,
                            code=code, number=number)
            course_dao.add(course)
            return course
        return None

    def update_course(self, course_id, name=None, description=None,
                      code=None, number=None):
        if (course_id is None):
            return False

        if (name is None) and (description is None)\
           and (code is None) and (number is None):
            return False

        try:
            course = course_dao.get_by_id(course_id=course_id)

            if name:
                course.name = name
            if description:
                course.description = description
            if code:
                course.code = code
            if number:
                course.number = number

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_course(self, course_id):
        if course_id is None:
            return False

        try:
            course = course_dao.get_by_id(course_id=int(course_id))
            if course:
                course_dao.delete_course_by_id(course_id)
                return True
            else:
                return False

        except Exception:
            return False


course_service = CourseService.get_instance()
