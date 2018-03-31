import os
path = os.path.abspath(os.path.dirname(__file__))

class Config():
    # 密钥
    SECRET_KEY = os.environ.get("SECRET", "123456")
    # 配置是否追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置是否默认提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 配置加载本地bootstrap样式
    BOOTSTRAP_SERVE_LOCAL = True
    # 配置图片上传
    MAX_CONTENT_LENGTH = 1024*1024*2
    UPLOADED_PHOTOS_DEST = path + "/static/uploads"

    # 配置smtp服务器
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = os.environ.get("MAIL_PORT", "465")
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", True)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
    # 用户名
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'manasseh_lost@qq.com')
    # 密码
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'nwbophxzucfggedd')





# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format("root", "Lz951231*", "127.0.0.1", "3306", "blog")


# 测试环境
class TestingConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(path, "blog-test.sqlite")


# 生产环境
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(path, "blog.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
