from alfred.dao.petitions import petition_dao, Petition, db


class PetitionService():
    __instance__ = None

    def __init__(self):
        if PetitionService.__instance__ is None:
            PetitionService.__instance__ = self
        else:
            raise Exception("You cannot create another PetitionService class")

    @staticmethod
    def get_instance():
        if not PetitionService.__instance__:
            PetitionService()
        return PetitionService.__instance__

    def create_petition(self, transcript, request_comment, date_submitted,
                        advisor_comment, decision_comment, date_decided):
        if (transcript is None) or (request_comment is None) or\
           (date_submitted is None) or (advisor_comment is None) or\
           (decision_comment is None) or (date_decided is None):
            return None

        petition = Petition(transcript=transcript,
                            request_comment=request_comment,
                            date_submitted=date_submitted,
                            advisor_comment=advisor_comment,
                            decision_comment=decision_comment,
                            date_decided=date_decided)
        petition_dao.add(petition)
        return petition

    def update_petition(self, petition_id, transcript=None,
                        request_comment=None,
                        date_submitted=None,
                        advisor_comment=None,
                        decision_comment=None,
                        date_decided=None):
        if (petition_id is None):
            return False

        if (transcript is None) and (request_comment is None) and\
           (date_submitted is None) and (advisor_comment is None) and\
           (decision_comment is None) and (date_decided is None):
            return False

        try:
            petition = petition_dao.get_by_id(petition_id=petition_id)

            if transcript:
                petition.transcript = transcript
            if request_comment:
                petition.request_comment = request_comment
            if date_submitted:
                petition.date_submitted = date_submitted
            if advisor_comment:
                petition.advisor_comment = advisor_comment
            if decision_comment:
                petition.decision_comment = decision_comment
            if date_decided:
                petition.date_decided = date_decided

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_petition(self, petition_id):
        if petition_id is None:
            return False

        try:
            petition = petition_dao.get_by_id(petition_id=int(petition_id))
            if petition:
                petition_dao.delete_petition_by_id(petition_id)
                return True
            else:
                return False

        except Exception:
            return False


petition_service = PetitionService.get_instance()
