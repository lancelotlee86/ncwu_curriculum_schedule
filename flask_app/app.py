from flask import Flask
from datetime import datetime

from flask_app.func_with_database import func_getCrowdednessRateByPosition
from flask_app.func_with_database import func_getNearbyPositionsByPosition
from flask_app.func_with_database import func_getCourseNameAndPositionByTimeAndPosition
from flask_app.func_with_database import func_getClassTimeByGivenTime
from flask_app.func_with_database import func_checkAccount

from flask_app.models import Classroom

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getCrowdednessRateByPosition/<position>")
def getCrowdednessRateByPosition(position):
    result = func_getCrowdednessRateByPosition(position)
    return str(result)


@app.route("/getNearbyCourseByPosition/<position>")
def getNearbyCourseByPosition(position):
    classroom = Classroom(position)
    nearby_positions = func_getNearbyPositionsByPosition(position)
    now = datetime.now()
    classTimeNow = func_getClassTimeByGivenTime(now)
    # test
    classTimeNow = func_getClassTimeByGivenTime(datetime(2010,10,28,9,30))
    print(classTimeNow)
    print(nearby_positions)
    nearby_courses = []
    for position in nearby_positions:
        if func_getCourseNameAndPositionByTimeAndPosition(position, classTimeNow):
            # 如果有返回记录的话
            course = func_getCourseNameAndPositionByTimeAndPosition(position, classTimeNow)
            nearby_courses.append(course)
    return str(nearby_courses)

@app.route("/checkAccount/<username>/<password>")
def checkAccount(username, password):
    if func_checkAccount(username, password):
        return '1'
    return '0'




if __name__ == "__main__":
    app.run()
