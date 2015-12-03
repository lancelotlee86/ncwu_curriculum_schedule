from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lishenzhi1214@localhost/curriculum_schedule_app'
db = SQLAlchemy(app)


class Classroom(db.Model):

    _id = None
    campus = None
    building = None
    floor = None
    number = None
    capacity = None
    _position = None


    def __init__(self, _id=None, _position=None):
        if(_id):
            record = c

    def getNearbyClassroom(self):
