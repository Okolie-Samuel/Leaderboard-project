from sqlalchemy import Table
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy



from src import db


class LeaderBoardTable(db.Model):
    __tablename__ = "Leaderboard"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(300))
    slack_id = db.Column(db.String(25))
    email = db.Column(db.String(60), unique=True,)
    total_points = db.Column(mysql.INTEGER(11), index=True)
 

    def __repr__(self):
        return "<User ((First name: %s - ID: %s))" % (self.first_name, self._id)




    