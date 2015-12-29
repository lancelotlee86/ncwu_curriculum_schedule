from flask import Flask, request, jsonify
from datetime import datetime

from flask_app.func_with_database import func_getCrowdednessRateByPosition
from flask_app.func_with_database import func_getNearbyPositionsByPosition
from flask_app.func_with_database import func_getCourseNameAndPositionByTimeAndPosition
from flask_app.func_with_database import func_getClassTimeByGivenTime
from flask_app.func_with_database import func_checkAccount

from flask_app.models import Classroom, Lesson, LessonTime, FryCourse

app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/get_crowdedness_rate_by_position")
def get_crowdedness_rate_by_position():
    position = request.args.get('position')
    classroom = Classroom(_position=position)
    crowdedness = classroom.crowdedness()['crowded_rate']
    return jsonify(crowdedness=crowdedness)


@app.route("/get_nearby_lessons_by_position")
def get_nearby_lessons_by_position():
    """
    返回给定教室和时间的附近的课，这个方法默认当前访问时间
    :param
    :return:
    """
    position = request.args.get('position')
    lessontime = request.args.get('lessontime')

    classroom = Classroom(_position=position)
    #lessontime = '20102011-1-11-3-1'
    if lessontime:
        lesson = Lesson(clsrm_id=classroom.clsrm_id, _datetime_string=lessontime)
    else:
        now = datetime.now()
        lesson = Lesson(clsrm_id=classroom.clsrm_id, _datetime=now)

    nearby_lessons = lesson.nearby_lessons()
    re = []
    for lesson in nearby_lessons:
        re.append({'name': lesson.name, 'position': lesson._position})
    return jsonify(lessons=re)

@app.route("/check_account/<username>/<password>")
def checkAccount(username, password):
    if func_checkAccount(username, password):
        return '1'
    return '0'


@app.route("/static_lessons")
def static_lessons():
    ''' 这里的 lessons 指的是 fry_courses'''
    class_id = "2009003"    # 暂时这么用，稍后再加入token提取请求的class
    static_lessons = Lesson.static_lessons(class_id)    # 现在 static_lessons 是所有的给定班级的lessons
    # 这个 static_lessons 实际上是一个 generater,我换成列表会出错
    fry_courses = FryCourse.multiple_fry_courses(static_lessons)    # 这里得到的 fry_courses 是fry_courses的序列
    fry_courses_json = []
    for fry_course in fry_courses:
        fry_course_json = {}
        fry_course_json['course_id'] = fry_course.fry_course_id
        fry_course_json['name'] = fry_course.fry_course_name
        fry_course_json['teacher'] = fry_course.fry_course_teacher
        fry_course_json['schedule'] = fry_course.fry_course_schedule
        fry_courses_json.append(fry_course_json)
    return jsonify(courses=fry_courses_json)


if __name__ == "__main__":
    app.run(host='localhost', port=8081, debug=True)