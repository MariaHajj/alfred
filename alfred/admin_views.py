from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from alfred.models import Major


# Show null values instead of empty strings.
MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({type(None): typefmt.null_formatter})


class UserView(ModelView):
    form_columns = (
        'aub_id',
        'email',
        'first_name',
        'last_name',
        'password',
        'role',
        'advisor',
        'major'
    )
    column_sortable_list = ('first_name', ('major', 'major.id', 'id'))
    column_searchable_list = ('aub_id', 'email', 'first_name',
                              'last_name', Major.code)
    column_filters = ('aub_id', 'major')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class RoleView(ModelView):
    pass


class AnnouncementView(ModelView):
    pass


class FacultyView(ModelView):
    pass


class DepartmentView(ModelView):
    pass


class MajorView(ModelView):
    pass


class CourseView(ModelView):
    pass


class CourseAvailabilityView(ModelView):
    pass


class AvailabilityView(ModelView):
    pass


class FrequencyView(ModelView):
    pass


class TermView(ModelView):
    pass


class CourseGradeView(ModelView):
    pass


class CapacitySurveyView(ModelView):
    pass


class PetitionView(ModelView):
    pass


class PetitionTypeView(ModelView):
    pass


class PetitionStatusView(ModelView):
    pass
