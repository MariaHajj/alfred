from alfred.models import Term
from alfred import db


class TermDAO():
    """Class to handle all database operations
    for models.Term class.
    """
    __instance__ = None

    def __init__(self):
        if TermDAO.__instance__ is None:
            TermDAO.__instance__ = self
        else:
            raise Exception("You cannot create another TermDAO class")

    @staticmethod
    def get_instance():
        if not TermDAO.__instance__:
            TermDAO()
        return TermDAO.__instance__

    def add(self, term):
        db.session.add(term)
        db.session.commit()

    def get_all(self):
        return db.session.query(Term).all()

    def get_by_id(self, term_id):
        return db.session.query(Term).get(term_id)

    def get_by_name(self, name):
        return db.session.query(Term).filter_by(name=name).first()

    def delete_term_by_id(self, term_id):
        db.session.query(Term).filter_by(id=term_id).delete()
        db.session.commit()


term_dao = TermDAO.get_instance()
