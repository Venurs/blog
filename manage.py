from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand
from flaskext.markdown import Markdown, Extension

app = create_app("default")
md = Markdown(app)
manage = Manager(app=app)

# 添加迁移命令
manage.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manage.run()