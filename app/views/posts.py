from flask import Flask, Blueprint, render_template
from app.forms import PostsForm, BlogForm

post = Blueprint("posts", __name__)


@post.route("/editor_blog/", methods=["get", "post"])
def editor_blog():
    form = BlogForm()
    if form.validate_on_submit():
        pass
    return render_template("editor_blog.html")