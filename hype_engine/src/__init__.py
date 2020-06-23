from flask import Flask
from hype_engine.src.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__,  template_folder='templates')
    app.config.from_object(Config)
    # db.init_app(app)
    # migrate = Migrate(app, db)


    with app.app_context():
        from . import routes
        # db.create_all()
    return app