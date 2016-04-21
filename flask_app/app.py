#encoding=utf-8
from flask import Flask, request, jsonify, abort
from datetime import datetime, timedelta
import uuid

from flask_app.func_with_database import func_insertCrowdednessRateByPosition

from flask_app.models import Classroom, Lesson, LessonTime, FryCourse, Student

app = Flask(__name__)
app.debug = True



@app.route("/")
def hello():
    return str(tokens)


# API----获取token
'''
参数：
{
    "userid": (string),
    "password": (string)
}
返回值：
{
    "token": <string>
}
'''
@app.route("/token")
def token():
    user_id = request.args.get('userid')
    # 先根据给定的id创建对应的用户对象
    if not user_id:
        abort(404)
    if len(user_id) == 9:   # 学生
        user = Student(user_id)
        pass
        if not user:
            abort(404)
    else:
        pass    # 教师的暂时没写
    # 检测提交的密码和本地存储的密码是否一样
    if user.password != request.args.get('password'):
        abort(404)
    token = str(uuid.uuid1())   # 生成随机且唯一的字符串
    tokens[token] = user.id     # 将随机字符串作为键，用户id作为值，存储在tokens字典中。
    # 以后有空了将这个换成专门的键值对数据库
    return jsonify(token=token)


# API----按教室获取拥挤度信息
'''
参数: { token: <string> } 其实这个token有没有都行
'''
@app.route("/<position>/crowdedness")
def get_crowdedness_rate_by_position(position):
    if position[0] == '1':
        position = '[龙]一号楼' + position
    elif position[0] == '2':
        position = '[龙]二号楼' + position
    elif position[0] == '3':
        position = '[龙]三号楼' + position
    elif position[0] == '4':
        position = '[龙]四号楼' + position
    elif position[0] == '5':
        position = '[龙]五号楼' + position
    classroom = Classroom(_position=position)
    crowdedness = classroom.crowdedness()['crowded_rate']
    return jsonify(crowdedness=crowdedness)


# API----按教室更新拥挤度信息
'''
参数:
{
    "token": (string),
    "crowdedness": (num)
}
返回值：状态码
'''
@app.route("/<position>/crowdedness", methods=['POST'])
def post_crowdedness_rate_by_position(position):
    crowdedness_rate = request.args.get('crowdedness')
    func_insertCrowdednessRateByPosition(crowdedness_rate, position)
    return '200'



# API----获取附近的课
'''
参数：
{
    "token"： (string),
    "lesson_time": (string)    // 可有可无，见下面的说明
}
返回值： 一个json对象
{
  "lessons": [
    {
      "name": (string),
      "teacher": (string),
      "position": (string),
      "fry_course_id": (string)
    },
    {
      "name": (string),
      "teacher": (string),
      "position": (string),
      "fry_course_id": (string)
    }
  ]
}
'''
@app.route("/<position>/nearby_lessons")
def position_nearby_lessons(position):
    """
    返回给定教室和时间的附近的课，这个方法默认当前访问时间
    :param
    :return:
    """
    position = position
    lesson_time = request.args.get('lesson_time')

    # 首先实例化给定教室对应的Classroom对象
    classroom = Classroom(_position=position)
    # 接着实例化给定或者当前时间与教室共同决定的Lesson对象，代表某个时间在某个教室上的课
    #lesson_time = '20102011-1-11-3-1'
    if lesson_time:     # 参数中给定了时间
        lesson = Lesson(clsrm_id=classroom.clsrm_id, _datetime_string=lesson_time)
    else:   # 参数中没有给定时间，使用当前时间
        now = datetime.now()
        then = now + timedelta(minutes = 60) # 直接加上60分钟好了，临时这么做，因为客户端不好修改。
        lesson = Lesson(clsrm_id=classroom.clsrm_id, _datetime=then)

    # 通过一个Lesson对象的静态方法，得到附近的课的序列，最后处理一下数据返回
    nearby_lessons = lesson.nearby_lessons()
    re = []     # return
    for lesson in nearby_lessons:
        re.append({'name': lesson.name, 'position': lesson._position})
    return jsonify(lessons=re)


# API----获取某个班的固定课程，课程表（教学计划）
'''
参数:     { token: (string) }
返回值： 是包含着fry_course的序列
{
    courses:
    [
        {
            "course_id": (string),
            "name": (string),
            "teacher": (string),
            "schedule":
            [
                {
                    "week": (num),
                    "weekday": (num),
                    "class_index": (num)
                },
                ...
            ]
        },
        {
            ...
        }
    ]
}
'''
@app.route("/static_lessons")
def static_lessons():
    ''' 这里的 lessons 指的是 fry_courses'''

    # token 验证
    if request.args.get("token") not in tokens:
        abort(404)
    else:
        user_id = tokens[request.args.get("token")]

    # 通过class_id获取这个班要上的所有课程
    class_id = user_id[0:7]
    static_lessons = Lesson.static_lessons(class_id)    # 现在 static_lessons 是所有的给定班级的lessons
    # 这个 static_lessons 实际上是一个 generater,我换成列表会出错
    fry_courses = FryCourse.multiple_fry_courses(static_lessons)    # 这里得到的 fry_courses 是fry_courses的序列
    # 这里得到的 fry_courses 序列中的成员是FryCourse类的对象

    # 下面要将其转换成普通的 dict，这样才能将其 json 化
    fry_courses_json = []
    for fry_course in fry_courses:
        fry_course_json = {}
        fry_course_json['course_id'] = fry_course.fry_course_id
        fry_course_json['name'] = fry_course.fry_course_name
        fry_course_json['teacher'] = fry_course.fry_course_teacher
        fry_course_json['schedule'] = fry_course.fry_course_schedule
        fry_courses_json.append(fry_course_json)
    return jsonify(courses=fry_courses_json[0:50])



# API----获取课程表（个性化课程）
'''
参数：	`token: (string)`
返回值： FryCourse的对象的序列
'''
@app.route("/mylessons", methods=['GET'])
def get_mylessons():
    ''' 这里的 lessons 指的是 fry_courses'''

    # token 验证
    if request.args.get("token") not in tokens:
        abort(404)
    else:
        user_id = tokens[request.args.get("token")]

    # 得到token代表的学生对象
    student_id = user_id
    stu = Student(student_id)
    fry_courses_id = stu.fry_courses_id # 这里的fry_courses_id其实就是数据库中student表的mycourses列

    # 将这个学生的自己的fry_courses_id（mycourses）实例化成对相爱
    fry_courses = []
    for fry_course_id in fry_courses_id:
        fry_courses.append( FryCourse.fry_course_by_fry_course_id(fry_course_id))

    # 将上面那个对象实例化转化成可以json化的字典序列并返回
    fry_courses_json = []
    for fry_course in fry_courses:
        fry_course_json = {}
        fry_course_json['course_id'] = fry_course.fry_course_id
        fry_course_json['name'] = fry_course.fry_course_name
        fry_course_json['teacher'] = fry_course.fry_course_teacher
        fry_course_json['schedule'] = fry_course.fry_course_schedule
        fry_courses_json.append(fry_course_json)
    return jsonify(courses=fry_courses_json)



# API----添加课程（个性化课程），只能一节一节课添加
'''
参数：
{
    "token":（string）,
    "course_id": (num),
}
返回值：`状态码200或204`
'''
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

    return '200'    # 这里应该返回状态码，但不是这种字符串形式的，稍后我研究下怎么弄


# API----删除课程（个性化课程）,只能一节一节课的删除
'''
参数：	token=(string)
返回值：`状态码200或204`
'''
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
    # 先生成一个内存中的tokens字典序列，其中包含一个测试用的token
    tokens = {"backdoor_token": "200900101"}
    app.run(host='0.0.0.0', port=8081, debug=True)