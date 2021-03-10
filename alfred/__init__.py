from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from alfred.config import BaseConfig


db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


#   Below import is necessary, even if the linter complains about it.
#   This is because the linter cannot distinguish between imports in a script
#   and imports in a package. The order of the imports is also important.
#   These two imports *had* to happen after initializing db.
from alfred.models import Role, Major, Department, Faculty, User
from alfred.models import CourseAvailability, Announcement, Course
from alfred.models import CourseGrade, Term, Frequency, Availability
from alfred.models import CapacitySurvey, Petition, PetitionType
from alfred.models import PetitionStatus

from flask_admin import Admin
from alfred.admin_views import DepartmentView, FacultyView, UserView
from alfred.admin_views import MajorView, RoleView, AnnouncementView
from alfred.admin_views import CourseView, CourseAvailabilityView
from alfred.admin_views import AvailabilityView, FrequencyView, TermView
from alfred.admin_views import CourseGradeView, CapacitySurveyView
from alfred.admin_views import PetitionView, PetitionTypeView
from alfred.admin_views import PetitionStatusView


admin = Admin(name='alfred Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(FacultyView(Faculty, db.session))
admin.add_view(DepartmentView(Department, db.session))
admin.add_view(MajorView(Major, db.session))
admin.add_view(CourseView(Course, db.session))
admin.add_view(AnnouncementView(Announcement, db.session))
admin.add_view(TermView(Term, db.session))
admin.add_view(FrequencyView(Frequency, db.session))
admin.add_view(AvailabilityView(Availability, db.session))
admin.add_view(CourseAvailabilityView(CourseAvailability, db.session))
admin.add_view(CourseGradeView(CourseGrade, db.session))
admin.add_view(CapacitySurveyView(CapacitySurvey, db.session))
admin.add_view(PetitionTypeView(PetitionType, db.session))
admin.add_view(PetitionStatusView(PetitionStatus, db.session))
admin.add_view(PetitionView(Petition, db.session))


# Image dimensions
MAX_HEIGHT = 400
MAX_WIDTH = 400


def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    from alfred.core.users.views import users
    from alfred.core.main.routes import main

    from alfred.core.errors.handlers import errors

    from alfred.core import blueprint as api
    app.register_blueprint(api, url_prefix='/api/1')

    app.register_blueprint(main)
    app.register_blueprint(errors)

    app.register_blueprint(users)

    return app
