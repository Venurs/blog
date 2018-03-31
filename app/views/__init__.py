from .user import user
from .main import main
from .posts import post
from .blogs import blogs

DEFAULT_BULEPRINT = (
    (user, "/user"),
    (main, "/main"),
    (post, "/posts"),
    (blogs, "/blogs"),
)


def config_blueprint(app):
    for blueprint, url_prefix in DEFAULT_BULEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
