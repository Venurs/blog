from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import Length, DataRequired
from app.models import Classify


class PostsForm(FlaskForm):
    content = TextAreaField("评论", render_kw={"style":"resize:none","style":"resize:none","rows":5, "placeholder":"请发表你的评论"},
                            validators=[DataRequired(), Length(6,120,message="长度不能超过120个字符")])
    submit = SubmitField("发表")


class BlogForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired(message="标题不能为空")])
    classify = SelectField("分类", coerce=int, choices=[], validators=[DataRequired(message="类别不能为空")])
    abstract = StringField("摘要", validators=[DataRequired(message="摘要不能为空"),Length(6,150,message="摘要长度不能超过150个字符")])
    content = TextAreaField("博客",validators=[DataRequired(message="博客内容不能空")])
    submit = SubmitField("发表")
