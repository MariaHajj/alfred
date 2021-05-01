from alfred.dao.terms import term_dao, Term, db


class TermService():
    __instance__ = None

    def __init__(self):
        if TermService.__instance__ is None:
            TermService.__instance__ = self
        else:
            raise Exception("You cannot create another TermService class")

    @staticmethod
    def get_instance():
        if not TermService.__instance__:
            TermService()
        return TermService.__instance__

    def create_term(self, name, start_date, end_date):
        if (name is None) or (start_date is None) or (end_date is None):
            return None

        term = term_dao.get_by_name(name=name)
        if term is None:
            term = Term(name=name, start_date=start_date, end_date=end_date)
            term_dao.add(term)
            return term
        return None

    def update_term(self, term_id, name=None, start_date=None, end_date=None):
        if (term_id is None):
            return False

        if (name is None) and (start_date is None) and (end_date is None):
            return False

        try:
            term = term_dao.get_by_id(term_id=term_id)

            if name:
                term.name = name
            if start_date:
                term.start_date = start_date
            if end_date:
                term.start_date = start_date

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_term(self, term_id):
        if term_id is None:
            return False

        try:
            term = term_dao.get_by_id(term_id=int(term_id))
            if term:
                term_dao.delete_term_by_id(term_id)
                return True
            else:
                return False

        except Exception:
            return False


term_service = TermService.get_instance()
