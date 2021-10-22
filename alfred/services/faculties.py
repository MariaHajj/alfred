from alfred.dao.faculties import faculty_dao, Faculty, db


class FacultyService():
    __instance__ = None

    def __init__(self):
        if FacultyService.__instance__ is None:
            FacultyService.__instance__ = self
        else:
            raise Exception("You cannot create another FacultyService class")

    @staticmethod
    def get_instance():
        if not FacultyService.__instance__:
            FacultyService()
        return FacultyService.__instance__

    def create_faculty(self, name, code):
        if (name is None) or (code is None):
            return None

        faculty = faculty_dao.get_by_name(name=name)
        if faculty is None:
            faculty = Faculty(name=name, code=code)
            faculty_dao.add(faculty)
            return faculty
        return None

    def update_faculty(self, faculty_id, name=None, code=None):
        if (faculty_id is None):
            return False

        if (name is None) and (code is None):
            return False

        try:
            faculty = faculty_dao.get_by_id(faculty_id=faculty_id)

            if name:
                faculty.name = name
            if code:
                faculty.code = code

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_faculty(self, faculty_id):
        if faculty_id is None:
            return False

        try:
            faculty = faculty_dao.get_by_id(faculty_id=int(faculty_id))
            if faculty:
                faculty_dao.delete_faculty_by_id(faculty_id)
                return True
            else:
                return False

        except Exception:
            return False


faculty_service = FacultyService.get_instance()
