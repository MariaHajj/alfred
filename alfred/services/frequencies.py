from alfred.dao.frequencies import frequency_dao, Frequency, db


class FrequencyService():
    __instance__ = None

    def __init__(self):
        if FrequencyService.__instance__ is None:
            FrequencyService.__instance__ = self
        else:
            raise Exception("You cannot create another FrequencyService class")

    @staticmethod
    def get_instance():
        if not FrequencyService.__instance__:
            FrequencyService()
        return FrequencyService.__instance__

    def create_frequency(self, value, description):
        if (value is None) or (description is None):
            return None

        frequency = frequency_dao.get_by_value(value=value)
        if frequency is None:
            frequency = Frequency(value=value, description=description)
            frequency_dao.add(frequency)
            return frequency
        return None

    def update_frequency(self, frequency_id, value=None, description=None):
        if (frequency_id is None):
            return False

        if (value is None) and (description is None):
            return False

        try:
            frequency = frequency_dao.get_by_id(frequency_id=frequency_id)

            if value:
                frequency.value = value
            if description:
                frequency.description = description

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_frequency(self, frequency_id):
        if frequency_id is None:
            return False

        try:
            frequency = frequency_dao.get_by_id(frequency_id=int(frequency_id))
            if frequency:
                frequency_dao.delete_frequency_by_id(frequency_id)
                return True
            else:
                return False

        except Exception:
            return False


frequency_service = FrequencyService.get_instance()
