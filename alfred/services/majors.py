from alfred.dao.majors import major_dao, Major, db


class MajorService():
    __instance__ = None

    def __init__(self):
        if MajorService.__instance__ is None:
            MajorService.__instance__ = self
        else:
            raise Exception("You cannot create another MajorService class")

    @staticmethod
    def get_instance():
        if not MajorService.__instance__:
            MajorService()
        return MajorService.__instance__

    def create_major(self, name, code):
        if (name is None) or (code is None):
            return None

        major = major_dao.get_by_name(name=name)
        if major is None:
            major = Major(name=name, code=code)
            major_dao.add(major)
            return major
        return None

    def update_major(self, major_id, name=None, code=None):
        if (major_id is None):
            return False

        if (name is None) and (code is None):
            return False

        try:
            major = major_dao.get_by_id(major_id=major_id)

            if name:
                major.name = name
            if code:
                major.code = code

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_major(self, major_id):
        if major_id is None:
            return False

        try:
            major = major_dao.get_by_id(majorr_id=int(major_id))
            if major:
                major_dao.delete_major_by_id(major_id)
                return True
            else:
                return False

        except Exception:
            return False


major_service = MajorService.get_instance()
