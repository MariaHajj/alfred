from alfred import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_validator import ValidateEmail
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from datetime import datetime, timezone


@login_manager.user_loader
def load_user(user_id):
    """Get the current logged-in User object.

    Parameters
    ----------
    user_id : [int]
        User ID.

    Returns
    -------
    [User]
        A User object (see alfred.models).
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    aub_id = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    image_file = db.Column(db.String(30),
                           nullable=False,
                           default='default.jpg')

    _password = db.Column(db.String(128), nullable=False)

    announcement = db.relationship('Announcement', back_populates='user')

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    advisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    advisor = db.relationship('User', remote_side=[id])

    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    major = db.relationship('Major')

    petition = db.relationship('Petition', back_populates='user')

    course_grade = db.relationship('CourseGrade', back_populates='user')

    def __repr__(self):
        return (f"'{self.first_name} {self.last_name}', '{self.email}'\
                       '{self.aub_id}', {self.major}")

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    @classmethod
    def __declare_last__(cls):
        # check_deliverability can be set to True
        # after the developer updated the release on PyPI.
        # https://github.com/xeBuz/Flask-Validator/issues/79
        ValidateEmail(User.email,
                      allow_smtputf8=True,
                      check_deliverability=True,
                      throw_exception=True,
                      message="The e-mail is invalid.")


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), unique=True, nullable=False)

    # The role marked as default will be the one assigned to new users
    # upon registration. Since the application is going to search
    # the roles table to find the default one, this column is configured
    # to have an index, as that will make searches much faster.
    # default = db.Column(db.Boolean, default=False, index=True)

    # permissions field, which is an integer value that defines the list
    # of permissions for the role in a compact way (for later setup)
    # permissions = db.Column(db.Integer)

    users = db.relationship('User', back_populates='role', lazy='dynamic')

    def __init__(self, title, description, user):
        self.title = title
        self.description = description
        self.user = user

    def __repr__(self):
        return(f"{self.User}'s role: {self.title}")


class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(45), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    upload_date = db.Column(db.DateTime,
                            default=datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='announcement')

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return(f"{self.title}"
               f" uploaded on {self.upload_date}\n"
               f"{self.description}")


class Faculty(db.Model):
    __tablename__ = 'faculty'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(70), unique=True, nullable=False)
    code = db.Column(db.String(5), unique=True, nullable=False)

    department = db.relationship('Department', back_populates='faculty')

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return(f"Faculty of {self.name} ({self.code})")


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(70), unique=True, nullable=False)
    code = db.Column(db.String(5), unique=True, nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = db.relationship('Faculty', back_populates='department')

    major = db.relationship('Major', back_populates='department')

    course = db.relationship('Course', back_populates='department')

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return(f"Department of {self.name} ({self.code})")


class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(70), unique=True, nullable=False)
    code = db.Column(db.String(5), unique=True, nullable=False)

    users = db.relationship('User')

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department')

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return(f"Major: {self.name} ({self.code})")


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    code = db.Column(db.String(5), unique=False, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', back_populates='course')

    capacity_survey = db.relationship('CapacitySurvey',
                                      back_populates='course')

    petition = db.relationship('Petition', back_populates='course')

    course_grade = db.relationship('CourseGrade', back_populates='course')

    course_availability = db.relationship('CourseAvailability',
                                          back_populates='course')

    def __init__(self, name, description, code, number):
        self.name = name
        self.description = description
        self.code = code
        self.number = number

    def __repr__(self):
        return(f"{self.code} {self.number}: {self.name}")

    @validates('course')
    def validate_course_code(self, code):
        if len(code) != 4:
            raise AssertionError('Code must be 4 characters')


class CourseAvailability(db.Model):
    __tablename__ = 'course_availability'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', back_populates='course_availability')

    availability_id = db.Column(db.Integer, db.ForeignKey('availability.id'))
    availability = db.relationship('Availability',
                                   back_populates='course_availability')

    def __init__(self, course, availability):
        self.course = course
        self.availability = availability

    def __repr__(self):
        return(f"Course: {self.course} | "
               f"Availability: {self.availability}")


class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    course_availability = db.relationship('CourseAvailability',
                                          back_populates='availability')

    frequency_id = db.Column(db.Integer, db.ForeignKey('frequency.id'))
    frequency = db.relationship('Frequency', back_populates='availability')

    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
    term = db.relationship('Term', back_populates='availability')

    def __init__(self, term, frequency):
        self.term = term
        self.frequency = frequency

    def __repr__(self):
        return(f"{self.term} | {self.frequency}")


class Frequency(db.Model):
    __tablename__ = 'frequency'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    value = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)

    availability = db.relationship('Availability', back_populates='frequency')

    def __init__(self, value, description):
        self.value = value
        self.description = description

    def __repr__(self):
        return(f"Frequency name: {self.value} | \n"
               f"Description: {self.description}")


class Term(db.Model):
    __tablename__ = 'term'
    __table_args__ = (CheckConstraint('end_date > start_date'),)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(45), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    availability = db.relationship('Availability', back_populates='term')

    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return(f"Term name: {self.name} | "
               f"Start date: {self.start_date} | "
               f"End date: {self.end_date}")


class CourseGrade(db.Model):
    __tablename__ = 'course_grade'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    value = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='course_grade')

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', back_populates='course_grade')

    def __init__(self, value, course):
        self.value = value
        self.course = course

    def __repr__(self):
        return(f"{self.user}: {self.course} grade = {self.value}")


class CapacitySurvey(db.Model):
    __tablename__ = 'capacity_survey'
    __table_args__ = (CheckConstraint('end_date > start_date'),)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(45), unique=False, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.String(500), unique=False, nullable=False)
    number_of_requests = db.Column(db.Integer, default='0')

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', back_populates='capacity_survey')
    students = db.relationship('StudentsRegisteredInSurveys',
                               backref='surveys')

    def __init__(self, title, start_date, end_date, comment):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.comment = comment

    def __repr__(self):
        return(f"{self.title} | "
               f"Open from {self.start_date} till {self.end_date}) | "
               f"{self.comment}")


class StudentsRegisteredInSurveys(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('capacity_survey.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, survey_id, student_id):
        self.survey_id = survey_id
        self.student_id = student_id


class Petition(db.Model):
    __tablename__ = 'petition'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    transcript = db.Column(db.String(100), nullable=False)
    request_comment = db.Column(db.String(500), unique=False, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow())
    decision_comment = db.Column(db.String(500), default=None)
    advisor_comment = db.Column(db.String(500), default=None)
    date_decided = db.Column(db.Date, default=None)

    petition_type_id = db.Column(db.Integer, db.ForeignKey('petition_type.id'))
    petition_type = db.relationship('PetitionType', back_populates='petition')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='petition')

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', back_populates='petition')

    petition_status_id = db.Column(db.Integer,
                                   db.ForeignKey('petition_status.id'))
    petition_status = db.relationship('PetitionStatus',
                                      back_populates='petition')

    def __init__(self, transcript, request_comment, date_submitted,
                 petition_type, course, petition_status, advisor_comment,
                 decision_comment, date_decided, user):
        self.transcript = transcript
        self.request_comment = request_comment
        self.date_submitted = date_submitted
        self.petition_type = petition_type
        self.course = course
        self.petition_status = petition_status
        self.advisor_comment = advisor_comment
        self.decision_comment = decision_comment
        self.date_decided = date_decided
        self.user = user


class PetitionType(db.Model):
    __tablename__ = 'petition_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    petition = db.relationship('Petition', back_populates='petition_type')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return(f"Petition type: {self.name} | "
               f"Description: {self.description}")


class PetitionStatus(db.Model):
    __tablename__ = 'petition_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500))

    petition = db.relationship('Petition', back_populates='petition_status')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return(f"Petition status: {self.name} | "
               f"Description: {self.description}")
