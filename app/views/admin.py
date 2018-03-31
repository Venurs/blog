from flask_admin.contrib.sqla import ModelView
from app.extensions import blog_admin, db
from app.models import User, Posts

# blog_admin.add_view(ModelView(User, db.session))
# blog_admin.add_view(ModelView(Posts, db.session))