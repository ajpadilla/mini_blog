import logging
import os

from flask import render_template, redirect, url_for, abort, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.models import Post
from . import admin_bp
from .forms import PostForm, UserAdminForm
from ..auth.decorators import admin_required
from ..auth.models import User

logger = logging.getLogger(__name__)

@admin_bp.route("/admin/")
@login_required
@admin_required
def index():
    return render_template("admin/index.html")

@admin_bp.route("/admin/posts/")
@login_required
@admin_required
def list_posts():
    posts = Post.get_all()
    return render_template("admin/posts.html", posts=posts)

@admin_bp.route("/admin/post", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        context = form.context.data
        image_name = None
        if 'post_image' in request.files:
            file = request.files['post_image']
            if file.filename:
                image_name = secure_filename(file.filename)
                image_dir = current_app.config['POST_IMAGE_DIR']
                os.makedirs(image_dir, exist_ok=True)
                file_path = os.path.join(image_dir, image_name)
                file.save(file_path)
        post = Post(user_id=current_user.id, title=title, context=context)
        post.image_name = image_name
        post.save()
        logger.info(f'Guardando nuevo post {title}')
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form)

@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_post_form(post_id):
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.context = form.content.data
        post.save()
        logger.info(f'Guardando el post {post_id}')
        return redirect(url_for('admin.list_posts'))
    logger.info(f'{post.context}')
    return render_template("admin/post_form.html", form=form, post=post)

@admin_bp.route("/admin/post/delete/<int:post_id>/", methods=['POST',])
@login_required
@admin_required
def delete_post(post_id):
    logger.info(f'Se va a aliminar el post {post_id}')
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    post.delete()
    logger.info(f'El post {post_id} ha sido eliminado')
    return redirect(url_for('admin.list_posts'))

@admin_bp.route("/admin/users/")
@login_required
@admin_required
def list_users():
    users = User.get_all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/admin/user/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def update_user_form(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        user.is_admin = form.is_admin.data
        user.save()
        logger.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user)

@admin_bp.route("/admin/user/delete/<int:user_id>", methods=['POST',])
@login_required
@admin_required
def delete_user(user_id):
    logger.info(f'Se ve a eliminar al usuario {user_id}')
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))