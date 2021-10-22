from alfred.models import CapacitySurvey
from alfred import db


class CapacitySurveyDAO():
    """Class to handle all database operations
    for models.CapacitySurvey class.
    """
    __instance__ = None

    def __init__(self):
        if CapacitySurveyDAO.__instance__ is None:
            CapacitySurveyDAO.__instance__ = self
        else:
            raise Exception("You cannot create another"
                            "CapacitySurveyDAO class")

    @staticmethod
    def get_instance():
        if not CapacitySurveyDAO.__instance__:
            CapacitySurveyDAO()
        return CapacitySurveyDAO.__instance__

    def add(self, capacity_survey):
        db.session.add(capacity_survey)
        db.session.commit()

    def get_all(self):
        return db.session.query(CapacitySurvey).all()

    def get_by_id(self, capacity_survey_id):
        return db.session.query(CapacitySurvey).get_or_404(capacity_survey_id)

    def get_by_title(self, title):
        return db.session.query(CapacitySurvey).filter_by(title=title).first()

    def get_by_comment(self, comment):
        return db.session.query(CapacitySurvey)\
            .filter_by(comment=comment).first()

    def delete_capacity_survey_by_id(self, capacity_survey_id):
        db.session.query(CapacitySurvey)\
          .filter_by(id=capacity_survey_id).delete()
        db.session.commit()


capacity_survey_dao = CapacitySurveyDAO.get_instance()
