import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'tEamHuStLeRs'
    # CSRF_ENABLED = True
    # CSRF_SESSION_KEY = "secret"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'leaderboard.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False 


