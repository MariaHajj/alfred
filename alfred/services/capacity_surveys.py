from alfred.dao.capacity_surveys import capacity_survey_dao, CapacitySurvey, db


class CapacitySurveyService():
    __instance__ = None

    def __init__(self):
        if CapacitySurveyService.__instance__ is None:
            CapacitySurveyService.__instance__ = self
        else:
            raise Exception("You cannot create another"
                            "CapacitySurveyService class")

    @staticmethod
    def get_instance():
        if not CapacitySurveyService.__instance__:
            CapacitySurveyService()
        return CapacitySurveyService.__instance__

    def create_capacity_survey(self, title, start_date, end_date,
                               number_of_requests, comment):
        if (title is None) or (start_date is None) or (end_date is None)\
           or (number_of_requests is None) or (comment is None):
            return None

        capacity_survey = CapacitySurvey(title=title,
                                         start_date=start_date,
                                         end_date=end_date,
                                         number_of_requests=number_of_requests,
                                         comment=comment)
        capacity_survey_dao.add(capacity_survey)
        return capacity_survey

    def update_capacity_survey(self, capacity_survey_id, title=None,
                               start_date=None, end_date=None,
                               number_of_requests=None, comment=None):
        if (capacity_survey_id is None):
            return False

        if (title is None) and (start_date is None) and (end_date is None)\
           and (number_of_requests is None) and (comment is None):
            return False

        try:
            capacity_survey = capacity_survey_dao\
                .get_by_id(capacity_survey_id=capacity_survey_id)

            if title:
                capacity_survey.title = title
            if start_date:
                capacity_survey.start_date = start_date
            if end_date:
                capacity_survey.end_date = end_date
            if number_of_requests:
                capacity_survey.number_of_requests = number_of_requests
            if comment:
                capacity_survey.comment = comment

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_capacity_survey(self, capacity_survey_id):
        if capacity_survey_id is None:
            return False

        try:
            capacity_survey = capacity_survey_dao\
                .get_by_id(capacity_survey_id=int(capacity_survey_id))
            if capacity_survey:
                capacity_survey_dao\
                    .delete_capacity_survey_by_id(capacity_survey_id)
                return True
            else:
                return False

        except Exception:
            return False


capacity_survey_service = CapacitySurveyService.get_instance()
