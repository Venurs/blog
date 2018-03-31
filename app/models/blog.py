from app.extensions import db
from datetime import datetime
from flask_login import current_user
from markdown import markdown
import bleach


class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    make_time = db.Column(db.DateTime, default=datetime.utcnow())
    classify = db.relationship("Classify", backref="classify", lazy="joined", uselist=False)
    classify_id = db.Column(db.Integer, db.ForeignKey("classify.id"))
    content = db.Column(db.Text, nullable=False)
    abstract = db.Column(db.String(150), nullable=False)
    read_count = db.Column(db.Integer, default=0)

class Classify(db.Model):
    __tablename__ = "classify"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
