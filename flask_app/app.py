from flask import Flask, request, jsonify, abort
from datetime import datetime
import uuid

#from flask_app.func_with_database import func_checkAccount

from flask_app.models import Classroom, Lesson, LessonTime, FryCourse, Student

app = Flask(__name__)
app.debug = True



@app.route("/")
def hello():
    return str(tokens)

@app.route("/token")
def token():
    user_id = request.args.get('userid')
    if not user_id:
        abort(404)
    if len(user_id) == 9:   # 学生
        user = Student(user_id)
        if not user:
            abort(404)
    else:
        pass    # 教师的暂时没写
    if user.password != request.args.get('password'):
        abort(404)
    token = str(uuid.uuid1())
    tokens[token] = user.id
    return jsonify(token=token)

@app.route("/get_crowdedness_rate_by_position")
def get_crowdedness_rate_by_position():
    position = request.args.get('position')
    classroom = Classroom(_position=position)
    crowdedness = classroom.crowdedness()['crowded_rate']
    return jsonify(crowdedness=crowdedness)


@app.route("/<position>/nearby_lessons")
def position_nearby_lessons(position):
    """
    返回给定教室和时间的附近的课，这个方法默认当前访问时间
    :param
    :return:
    """
    position = position
    lesson_time = request.args.get('lesson_time')

    classroom = Classroom(_position=position)
    #lesson_time = '20102011-1-11-3-1'
    if lesson_time:
        lesson = Lesson(clsrm_id=classroom.clsrm_id, _datetime_string=lesson_time)
    else:
        now = datetime.now()
        lesson = Lesson(clsrm_id=classroom.clsrm_id, _datetime=now)

    nearby_lessons = lesson.nearby_lessons()
    re = []
    for lesson in nearby_lessons:
        re.append({'name': lesson.name, 'position': lesson._position})
    return jsonify(lessons=re)

"""
@app.route("/check_account/<username>/<password>")
def checkAccount(username, password):
    if func_checkAccount(username, password):
        return '1'
    return '0'
"""

@app.route("/static_lessons")
def static_lessons():
    ''' 这里的 lessons 指的是 fry_courses'''

    # token 验证
    if request.args.get("token") not in tokens:
        abort(404)
    else:
        user_id = tokens[request.args.get("token")]

    class_id = user_id[0:7]
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


@app.route("/mylessons", methods=['GET'])
def get_mylessons():
    ''' 这里的 lessons 指的是 fry_courses'''

    # token 验证
    if request.args.get("token") not in tokens:
        abort(404)
    else:
        user_id = tokens[request.args.get("token")]

    student_id = user_id
    stu = Student(student_id)
    fry_courses_id = stu.fry_courses_id

    fry_courses = []
    for fry_course_id in fry_courses_id:
        fry_courses.append( FryCourse.fry_course_by_fry_course_id(fry_course_id))

    fry_courses_json = []
    for fry_course in fry_courses:
        fry_course_json = {}
        fry_course_json['course_id'] = fry_course.fry_course_id
        fry_course_json['name'] = fry_course.fry_course_name
        fry_course_json['teacher'] = fry_course.fry_course_teacher
        fry_course_json['schedule'] = fry_course.fry_course_schedule
        fry_courses_json.append(fry_course_json)
    return jsonify(courses=fry_courses_json)

@app.route("/mylessons", methods=['POST'])
def post_mylessons():
    ''' 这里的 lessons 指的是 fry_courses'''

    # token 验证
    if request.args.get("token") not in tokens:
        abort(404)
    else:
        user_id = tokens[request.args.get("token")]
    if not request.args.get("course_id"):
        abort(404)
    else:
        fry_course_id = request.args.get("course_id")

    student_id = user_id

    stu = Student(student_id)
    stu.add_mycourse(fry_course_id=fry_course_id)

    return '200'

@app.route("/mylessons/<course_id>", methods=['DELETE'])
def delete_mylessons(course_id):
    ''' 这里的 lessons 指的是 fry_courses'''

    # token 验证
    if request.args.get("token") not in tokens:
        abort(404)
    else:
        user_id = tokens[request.args.get("token")]

    student_id = user_id
    fry_course_id = course_id    # '05100402008085'

    stu = Student(student_id)
    stu.delete_mycourse(fry_course_id=fry_course_id)

    return '200'


if __name__ == "__main__":
    tokens = {"backdoor_token": "200900101"}
    app.run(host='localhost', port=8081, debug=True)