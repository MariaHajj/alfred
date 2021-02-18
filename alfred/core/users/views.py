from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request

from alfred.core.users.forms import (RegistrationForm, LoginForm,
                                     UpdateAccountForm)
from flask_login import login_user, current_user, logout_user, login_required

from alfred.utils import save_image

from alfred.services.users import user_service
from alfred.dao.users import user_dao


users = Blueprint('users', __name__)


@users.route("/register",
             methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        aub_id = form.aub_id.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        # major = form.major.data
        password = form.password.data

        user_service.create_user(aub_id=aub_id, email=email.casefold(),
                                 first_name=first_name,
                                 last_name=last_name,
                                 #  major=major,
                                 password=password)

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html',
                           title='Register',
                           form=form)


@users.route("/login",
             methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = user_dao.get_by_email(email=form.email.data.casefold())
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page \
                else redirect(url_for('main.home'))
        else:
            flash("Login unsuccessful!", 'danger')

    return render_template('login.html',
                           title='Log in',
                           form=form)


@users.route("/logout",
             methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account",
             methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data, path="profile_pictures")
        else:
            image_file = None

        new_aub_id = form.aub_id.data
        new_first_name = form.first_name.data
        new_last_name = form.last_name.data

        user_id = current_user.id
        user_service.update_user(user_id=user_id, aub_id=new_aub_id,
                                 first_name=new_first_name,
                                 last_name=new_last_name,
                                 image_file=image_file)

        flash("Your account has been successfully updated!", 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.aub_id.data = current_user.aub_id
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.major.data = current_user.major

    image_file = url_for('static',
                         filename=f"profile_pictures/"
                                  f"{current_user.image_file}")

    return render_template('account.html',
                           title='Account',
                           image_file=image_file, form=form)
