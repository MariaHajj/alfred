from alfred.dao.users import user_dao, User, db


class UserService():
    __instance__ = None

    def __init__(self):
        if UserService.__instance__ is None:
            UserService.__instance__ = self
        else:
            raise Exception("You cannot create another UserService class")

    @staticmethod
    def get_instance():
        if not UserService.__instance__:
            UserService()
        return UserService.__instance__

    def create_user(self, aub_id, email, first_name,
                    last_name, major, password):
        if (aub_id is None) or (email is None) or (first_name is None) \
           or (last_name is None) or (major is None) or (password is None):
            return None

        user = user_dao.get_by_email(email=email)
        if user is None:
            user = User(aub_id=aub_id,
                        email=email.casefold(),
                        first_name=first_name,
                        last_name=last_name,
                        major=major,
                        password=password)
            user_dao.add(user)
            return user
        return None

    def update_user(self, user_id, aub_id=None, email=None,
                    first_name=None, last_name=None, image_file=None):
        if (user_id is None):
            return False

        if (aub_id is None) and (email is None) and (first_name is None) and \
           (last_name is None) and (image_file is None):
            return False

        try:
            user = user_dao.get_by_id(user_id=user_id)

            if aub_id:
                user.aub_id = aub_id
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if image_file:
                user.image_file = image_file

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_user(self, user_id):
        if user_id is None:
            return False

        try:
            user = user_dao.get_by_id(user_id=int(user_id))
            if user:
                user_dao.delete_user_by_id(user_id)
                return True
            else:
                return False

        except Exception:
            return False


user_service = UserService.get_instance()
