from alfred.dao.departments import department_dao, Department, db


class DepartmentService():
    __instance__ = None

    def __init__(self):
        if DepartmentService.__instance__ is None:
            DepartmentService.__instance__ = self
        else:
            raise Exception("You cannot create another\
                            DepartmentService class")

    @staticmethod
    def get_instance():
        if not DepartmentService.__instance__:
            DepartmentService()
        return DepartmentService.__instance__

    def create_department(self, name, code):
        if (name is None) or (code is None):
            return None

        department = department_dao.get_by_name(name=name)
        if department is None:
            department = Department(name=name, code=code)
            department_dao.add(department)
            return department
        return None

    def update_department(self, department_id, name=None, code=None):
        if (department_id is None):
            return False

        if (name is None) and (code is None):
            return False

        try:
            department = department_dao.get_by_id(department_id=department_id)

            if name:
                department.name = name
            if code:
                department.code = code

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_department(self, department_id):
        if department_id is None:
            return False

        try:
            department = department_dao\
                         .get_by_id(department_id=int(department_id))
            if department:
                department_dao.delete_department_by_id(department_id)
                return True
            else:
                return False

        except Exception:
            return False


department_service = DepartmentService.get_instance()
