from alfred.dao.petition_statuses import petition_status_dao,\
                                         PetitionStatus, db


class PetitionStatusService():
    __instance__ = None

    def __init__(self):
        if PetitionStatusService.__instance__ is None:
            PetitionStatusService.__instance__ = self
        else:
            raise Exception("You cannot create another"
                            "PetitionStatusService class")

    @staticmethod
    def get_instance():
        if not PetitionStatusService.__instance__:
            PetitionStatusService()
        return PetitionStatusService.__instance__

    def create_petition_status(self, name, description):
        if (name is None) or (description is None):
            return None

        petition_status = petition_status_dao.get_by_name(name=name)
        if petition_status is None:
            petition_status = PetitionStatus(name=name,
                                             description=description)
            petition_status_dao.add(petition_status)
            return petition_status
        return None

    def update_petition_status(self, petition_status_id,
                               name=None, description=None):
        if (petition_status_id is None):
            return False

        if (name is None) and (description is None):
            return False

        try:
            petition_status = petition_status_dao\
                .get_by_id(petition_status_id=petition_status_id)

            if name:
                petition_status.name = name
            if description:
                petition_status.description = description

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_petition_status(self, petition_status_id):
        if petition_status_id is None:
            return False

        try:
            petition_status = petition_status_dao\
                .get_by_id(petition_status_id=int(petition_status_id))
            if petition_status:
                petition_status_dao\
                    .delete_petition_status_by_id(petition_status_id)
                return True
            else:
                return False

        except Exception:
            return False


petition_status_service = PetitionStatusService.get_instance()
