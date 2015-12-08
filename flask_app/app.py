from flask import Flask
from datetime import datetime

from flask_app.func_with_database import func_getCrowdednessRateByPosition
from flask_app.func_with_database import func_getNearbyPositionsByPosition
from flask_app.func_with_database import func_getCourseNameAndPositionByTimeAndPosition
from flask_app.func_with_database import func_getClassTimeByGivenTime
from flask_app.func_with_database import func_checkAccount

from flask_app.models import Classroom, Lesson, LessonTime

app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/get_crowdedness_rate_by_position/<position>")
def get_crowdedness_rate_by_position(position):
    classroom = Classroom(_position=position)
    crowdedness = classroom.crowdedness()['crowded_rate']
    return str(crowdedness)


@app.route("/get_nearby_lessons_by_position/<position>")
def get_nearby_lessons_by_position(position):
    """
    返回给定教室和时间的附近的课，这个方法默认当前访问时间
    :param position:
    :return:
    """
    classroom = Classroom(_position=position)
    lessontime = '20102011-1-11-3-1'
    lesson = Lesson(clsrm_id=classroom.clsrm_id, _datetime_string=lessontime)
    nearby_lessons = lesson.nearby_lessons()
    re = []
    for lesson in nearby_lessons:
        re.append({'name': lesson.name, 'position': lesson._position})
    return str(re)

@app.route("/check_account/<username>/<password>")
def checkAccount(username, password):
    if func_checkAccount(username, password):
        return '1'
    return '0'




if __name__ == "__main__":
    app.run(host='localhost', port=8081, debug=True)