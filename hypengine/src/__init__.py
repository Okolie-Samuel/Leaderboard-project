from flask import Flask
from hypengine.src.config import Config

def create_app():
    app = Flask(__name__,  template_folder='templates')
    app.config.from_object(Config)



    with app.app_context():
        from . import routes
        # db.create_all()
    return app