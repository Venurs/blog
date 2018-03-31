from flask import Blueprint, render_template, url_for,current_app,redirect,send_from_directory
from app.forms import RegisterForm, LoginForm, UpdatePasswordForm, PhotoChangeForm
from app.models import User
from app.extensions import db,mail
from flask_mail import Message
from threading import Thread
from flask import flash,get_flashed_messages
from flask_login import login_user, logout_user, current_user
import os
import string
from PIL import Image
from uploads import photos
from .main import main
# from email import send_mail


user = Blueprint("user", __name__)


@user.route("/login/", methods=["get", "post"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash("当前用户不存在")
        elif not user.state:
            flash("帐号未激活")
        elif user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("登录成功")
            return redirect(url_for("main.index"))
        else:
            flash("请输入正确密码后登录")
        # return redirect(url_for("main.index"))
    return render_template("user/login.html", form=form)


@user.route("/register/", methods=["post", "get"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 数据写入数据库
        # 生成验证激活邮箱
        # 调用邮箱发送邮件
        # 给出提示信息，跳转至首页
        u = User(username=form.username.data,
                 password=form.password.data,
                 email=form.email.data)
        try:
            db.session.add(u)
            db.session.commit()
            token = u.make_avtive_token()
            send_mail(u.email, '账户激活', 'email/active', username=u.username, token=token)
            flash("邮件发送成功，请前往邮箱登录并激活")
            return redirect(url_for("main.index"))
        except:
            db.session.rollback()
            flash("注册失败")
    return render_template("user/register.html", form=form)


@user.route("/logout/")
def logout():
    logout_user()
    flash("退出登录成功，跳转至首页")
    return redirect(url_for("main.index"))


@user.route("/active/<token>")
def active(token):
    if User.check_token(token):
        flash("账户激活成功")
        return redirect(url_for("user.login"))
    else:
        flash("账户激活失败")
        return redirect(url_for("user.register"))


@user.route("/update_password/", methods=["get", "post"])
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            if not current_user.check_password(form.new_password.data):
                current_user.password = form.new_password.data
                try:
                    db.session.add(current_user)
                    db.session.commit()
                    flash("密码修改成功,请重新登录")
                    return redirect(url_for("user.logout"))
                except:
                    flash("密码修改失败")
                    db.session.rollback()
            else:
                flash("原密码和新的密码不能一致")
        else:
            flash("旧密码输入错误")
    return render_template("user/update_password.html", form=form)


@user.route("/update_photo/", methods=["get", "post"])
def update_photo():
    form = PhotoChangeForm()
    if form.validate_on_submit():
        photo_type = os.path.splitext(form.photo.data.filename)[1]
        filename = random_name(photo_type)
        photos.save(form.photo.data, name=filename)
        s_path = os.path.join(current_app.config["UPLOADED_PHOTOS_DEST"], filename)
        img = Image.open(s_path)
        img.thumbnail((130, 130))
        img.save(s_path)
        if current_user.photo_name != "img1.jpg":
            os.remove(os.path.join(current_app.config["UPLOADED_PHOTOS_DEST"], current_user.photo_name))
        current_user.photo_name = filename
        db.session.add(current_user)
    img_url = photos.url(current_user.photo_name)
    return render_template("user/photo_change.html", form=form, img_url=img_url)


@user.route("/show_photo/<filename>")
def show_photo(filename):
    return send_from_directory(current_app.config["UPLOADED_PHOTOS_DEST"], filename)


@user.route("/show_info/")
def show_info():
    return render_template("user/user_info.html")























def async_send_mail(app,msg):
    #发送邮件 获取 程序的上下文
    with app.app_context():
        mail.send(message=msg)


def send_mail(to,subject,template,**kwargs):
    #此刻的app就是外部实例化的app
    app = current_app._get_current_object()
    msg = Message(subject=subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    msg.html = render_template(template+'.html',**kwargs)
    # msg.body = render_template(template+'.txt')
    #发送邮件
    thr = Thread(target=async_send_mail,args=(app,msg))
    thr.start()
    return thr

# 生成随机的文件名
def random_name(photo_type, length=32):
    import random
    myString = string.ascii_letters + "0123456789"
    return ''.join(random.choice(myString) for i in range(length)) + photo_type
