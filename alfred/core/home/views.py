from flask import Blueprint, render_template
from alfred import db
from alfred.models import Announcement
from sqlalchemy import desc
from flask_login import login_required
from flask import redirect


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    announcements = Announcement.query\
        .order_by(desc(Announcement.upload_date)).all()
    return render_template('home.html', title='Home',
                           announcements=announcements)


@main.route("/catalogue")
@login_required
def catalogue():
    return render_template('catalogue.html', title="Catalogue")
