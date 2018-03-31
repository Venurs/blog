from app.extensions import db



# 用户收藏博客  多对多模型
class Collections(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    posts_id = db.Column(db.Integer, db.ForeignKey("posts.id"))



