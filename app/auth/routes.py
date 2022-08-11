import os

from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User
from .services import LoginFormService

@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        file = form.user_image.data
        image_name = None

        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['POST_IMAGE_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)

        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.image_name = image_name
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template("auth/signup_form.html", form=form, error=error)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    login_form_service = LoginFormService()
    form = login_form_service.get_form()

    if not login_form_service.is_validate_on_submit():
        return render_template('auth/login_form.html', form=form)

    user = User.get_by_email(login_form_service.get_email())

    if user is None or not user.check_password(login_form_service.get_password()):
        return render_template('auth/login_form.html', form=form)

    login_user(user, remember=login_form_service.get_remember_me())

    return redirect(url_for('public.index'))


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))