from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import ValidationError, DataRequired,EqualTo,Length,Email
from flask_wtf.file import FileField,FileAllowed,FileRequired
from uploads import photos
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(message="用户名不能为空"), Length(max=12,min=6,message="用户名长度为6到12位")])
    password = PasswordField("密码", validators=[DataRequired(),Length(6,12,message=("密码长度为6到12位"))])
    confirm = PasswordField("确认密码", validators=[DataRequired(),EqualTo("password", message="两次密码输入不一致")])
    images = FileField("头像", validators=[FileAllowed(photos, message=("该类型文件不允许上传"))])
    email = StringField("邮箱", validators=[DataRequired(),Email(message="请输入正确的邮箱格式")])
    submit = SubmitField("立即注册")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("该用户名已存在")

    def validate_email(self,field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("该邮箱已经被注册")


class LoginForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(message="用户名不能为空"), Length(max=12,min=6,message="用户名长度为6到12位")])
    password = PasswordField("密码", validators=[DataRequired(),Length(6,12,message=("密码长度为6到12位"))])
    remember = BooleanField("记住密码")
    submit = SubmitField("立即登录")


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField("原始密码", validators=[DataRequired(),Length(6,12,message=("密码长度为6到12位"))])
    new_password = PasswordField("新密码", validators=[DataRequired(),Length(6,12,message=("密码长度为6到12位"))])
    confirm_password = PasswordField("确认密码", validators=[DataRequired(),Length(6,12,message=("密码长度为6到12位")), EqualTo("new_password", message="密码输入不一致")])
    # verification_code = StringField("验证码",validators=[DataRequired(), Length(6,message="验证码必须是6位数字组成")])
    submit = SubmitField("提交")


class PhotoChangeForm(FlaskForm):
    photo = FileField("上传头像", validators=[DataRequired(), FileAllowed(photos, message=("该类型文件不被允许上传"))])
    submit = SubmitField("确认修改")




