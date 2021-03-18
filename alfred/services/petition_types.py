from alfred.dao.petition_types import petition_type_dao, PetitionType, db


class PetitionTypeService():
    __instance__ = None

    def __init__(self):
        if PetitionTypeService.__instance__ is None:
            PetitionTypeService.__instance__ = self
        else:
            raise Exception("You cannot create another"
                            "PetitionTypeService class")

    @staticmethod
    def get_instance():
        if not PetitionTypeService.__instance__:
            PetitionTypeService()
        return PetitionTypeService.__instance__

    def create_petition_type(self, name, description):
        if (name is None) or (description is None):
            return None

        petition_type = petition_type_dao.get_by_name(name=name)
        if petition_type is None:
            petition_type = PetitionType(name=name, description=description)
            petition_type_dao.add(petition_type)
            return petition_type
        return None

    def update_petition_type(self, petition_type_id,
                             name=None, description=None):
        if (petition_type_id is None):
            return False

        if (name is None) and (description is None):
            return False

        try:
            petition_type = petition_type_dao\
                .get_by_id(petition_type_id=petition_type_id)

            if name:
                petition_type.name = name
            if description:
                petition_type.description = description

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_petition_type(self, petition_type_id):
        if petition_type_id is None:
            return False

        try:
            petition_type = petition_type_dao\
                .get_by_id(petition_type_id=int(petition_type_id))
            if petition_type:
                petition_type_dao.delete_petition_type_by_id(petition_type_id)
                return True
            else:
                return False

        except Exception:
            return False


petition_type_service = PetitionTypeService.get_instance()
