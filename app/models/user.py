from app.extensions import db, login_manage
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize
from flask import current_app
from flask_login import UserMixin


class User(UserMixin,db.Model):
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True)
    password_hash = db.Column(db.String(128))
    photo_name = db.Column(db.String(40), default="img1.jpg")
    email = db.Column(db.String(60),unique=True)
    state = db.Column(db.Boolean, default=False)
    # 反向引用 参数1 反向引用的类名 参数2 反向引用字段名称 参数3 加载的时机 提供数据集的查询
    posts = db.relationship("Posts", backref="user", lazy="dynamic")
    blogs = db.relationship("Blog", backref="user", lazy="dynamic")
    favorites = db.relationship("Collections", backref="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("密码不可读")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def make_avtive_token(self):
        s = Seralize(current_app.config["SECRET_KEY"])
        return s.dumps({"id": self.id})

    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data["id"])
        if not user:
            return False
        elif not user.state:
            user.state = True
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
        return True

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manage.user_loader
def load_user(uid):
    return User.query.get(int(uid))