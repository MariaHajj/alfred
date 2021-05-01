from alfred.dao.announcements import announcement_dao, Announcement, db


class AnnouncementService():
    __instance__ = None

    def __init__(self):
        if AnnouncementService.__instance__ is None:
            AnnouncementService.__instance__ = self
        else:
            raise Exception("You cannot create another"
                            "AnnouncementService class")

    @staticmethod
    def get_instance():
        if not AnnouncementService.__instance__:
            AnnouncementService()
        return AnnouncementService.__instance__

    def create_announcement(self, title, description):
        if (title is None) or (description is None):
            return None

        announcement = Announcement(title=title, description=description)
        announcement_dao.add(announcement)
        return announcement

    def update_announcement(self, announcement_id, title=None,
                            description=None):
        if (announcement_id is None):
            return False

        if (title is None) and (description is None):
            return False

        try:
            announcement = announcement_dao\
                .get_by_id(announcement_id=announcement_id)

            if title:
                announcement.title = title
            if description:
                announcement.description = description

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_announcement(self, announcement_id):
        if announcement_id is None:
            return False

        try:
            announcement = announcement_dao\
                .get_by_id(announcement_id=int(announcement_id))
            if announcement:
                announcement_dao.delete_announcement_by_id(announcement_id)
                return True
            else:
                return False

        except Exception:
            return False


announcement_service = AnnouncementService.get_instance()
