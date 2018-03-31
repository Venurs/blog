from flask import Flask, Blueprint, render_template, redirect, url_for, request
from app.models import Posts
from app.forms import PostsForm
from flask import flash
from  app.extensions import db
from flask_login import current_user
from werkzeug.security import generate_password_hash,check_password_hash

main = Blueprint("main", __name__)


@main.route("/", methods=["get", "post"])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user = current_user._get_current_object()
            posts = Posts(content=form.content.data, user=user)
            db.session.add(posts)
        else:
            flash("你还没有登录，请前往登录页面登录")
            return redirect(url_for("user.login"))
    page = request.args.get("page", 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=2, error_out=False)
    posts_data = pagination.items
    return render_template("main/index.html", form=form, pagination=pagination, data=posts_data, viewFunc="main.index")
