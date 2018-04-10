from flask import Blueprint, render_template, url_for, redirect,request, jsonify, current_app, Response
from app.models import Blog, Posts
from app.models import Classify
from app.forms import BlogForm
from flask_login import current_user
from app.extensions import db
from flask import flash
from markdown import markdown
from app.forms import PostsForm
from .user import random_name
import bleach
import os

blogs = Blueprint("blog",__name__)

@blogs.route("/")
def test():
    return render_template("blog/test.html")


@blogs.route("/editor_blog/", methods=["get", "post"])
def editor_blog():
    form = BlogForm()
    classifies = Classify.query.filter()
    form.classify.choices += [(classify.id,classify.name) for classify in classifies]
    if current_user.is_authenticated:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            abstract = form.abstract.data
            classify = form.classify.data
            uid = current_user.id
            try:
                blog = Blog(title=title, content=content, abstract=abstract, classify_id=classify, uid=uid)
                db.session.add(blog)
                db.session.commit()
                flash("博客发表成功")
                return redirect(url_for("main.index"))
            except:
                db.session.rollback()
                flash("文章发表失败")
        return render_template("blog/editor_blog.html", classifies=classifies, form=form)
    else:
        flash("请登陆后发表博客")
        return render_template("blog/editor_blog.html", classifies=classifies, form=form)


@blogs.route("/show_blog_list/")
def show_blog_list():
    blogs = Blog.query.all()
    return render_template("blog/show_blog_list.html", blogs=blogs)


@blogs.route("/show_blog/<int:id>/", methods=["get", ])
def show_blog(id):
    # 计算阅读量
    blog = Blog.query.get(id)
    blog.read_count = blog.read_count + 1
    try:
        db.session.add(blog)
        db.session.commit()
    except:
        db.session.rollback()
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user = current_user._get_current_object()
            posts = Posts(content=form.content.data, user=user)
            db.session.add(posts)
        else:
            flash("你还没有登录，请前往登录页面登录后评论")
            return redirect(url_for("user.login"))
    page = request.args.get("page", 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=2,
                                                                                        error_out=False)
    posts_data = pagination.items
    return render_template("blog/show_blog.html", blog=blog, form=form, pagination=pagination, data=posts_data, viewFunc="main.index")


@blogs.route("/show_user_blog/")
def show_user_blog():
    blogs = Blog.query.filter(Blog.uid==current_user.id)
    return render_template("blog/show_user_blog.html", blogs=blogs)


@blogs.route("/blog_image/", methods=["post",])
def uploads_blog_image():
    image = request.files.get("editormd-image-file")
    # print(image)
    if not image:
        res = {
            "success": 0,
            "message": "图片上传异常",
        }
    else:
        ex = os.path.splitext(image.filename)[1]
        # print(ex)
        filename = os.path.join(random_name(ex))
        image.save(os.path.join(current_app.config["UPLOADED_BLOG_DEST"], filename))
        print("1")
        res = {
            "success:": 1,
            "message": "图片保存成功",
            "url": url_for("blog.image_save", filename=filename),
        }
        # print(res)
    return jsonify(res)


@blogs.route('/image_save/<filename>')
def image_save(filename):
    # blog_image = os.path.join(current_app.config["UPLOADED_BLOG_DEST"], filename)
    with open(os.path.join(current_app.config["UPLOADED_BLOG_DEST"], filename), mode="rb") as f:
        resp = Response(f.read(), mimetype="image/*")
    return resp











