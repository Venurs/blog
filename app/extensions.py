from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_admin import Admin
from flaskext.markdown import Markdown



bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate(db=db)
login_manage = LoginManager()
moment = Moment()
blog_admin = Admin(name="博客后台管理", template_mode="bootstrap3")

def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    login_manage.init_app(app)
    moment.init_app(app)
    blog_admin.init_app(app)
    #  指定登录的路由

    login_manage.login_view = "user.login"
    login_manage.login_message = "该页面需要登录后才能访问"
    login_manage.session_protection = "strong"