import pymysql.cursors
from datetime import datetime
from flask_app.sql_operation import *
from flask_app.config import startDayOfTheFirstTerm, startDayOfTheSecondTerm
from copy import deepcopy
import json

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lishenzhi1214',
                             db='curriculum_schedule_app',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class Classroom:

    clsrm_id = None
    campus = None
    building = None
    floor = None
    number = None
    capacity = None
    _position = None

    def __init__(self, clsrm_id=None, _position=None):
        if(clsrm_id):
            sql = sql_getClassroomById
        elif(_position):
            sql = sql_getClassroomByPosition
        else:
            sql = ''
        with connection.cursor() as cursor:
            cursor.execute(sql, clsrm_id if clsrm_id else _position)
            result = cursor.fetchone()
            self.clsrm_id = result['id']
            self.campus = result['campus']
            self.building = result['building']
            self.floor = result['floor']
            self.number = result['capacity']
            self._position = result['position']

    def __repr__(self):
        return '<Classroom %r>' % self._position

    def nearby_classrooms(self):
        ''' 返回当前对象代表教室的附近所有的教室, 返回的是对象列表
        :return:
        '''
        sql = sql_getNearbyPositionsByPosition
        with connection.cursor() as cursor:
            cursor.execute(sql, self._position)
            results = cursor.fetchall()
            # results 现在是一个字典列表，是这样的：[{'position': '六号楼6303'}, {'position': '六号楼6304'}, {'position': '六号楼6302'}]
            # 下面将其转换为简单的列表
            positions = []
            for result in results:
                positions.append(result['position'])
            # 现在的positions是这样的：['六号楼6303', '六号楼6304', '六号楼6302']
            # return positions
            nearby_classrooms = []
            for position in positions:
                nearby_classrooms.append(Classroom(_position=position))
            return nearby_classrooms

    def crowdedness(self):
        """
        返回当前教室对象的拥挤程度，字典
        :return:
        """
        sql = sql_getCrowdednessRateById
        with connection.cursor() as cursor:
            cursor.execute(sql, str(self.clsrm_id))
            result = cursor.fetchone()
            return result

    def post_crowdedness(self):
        """
        提交一条新的教室拥挤的的数据
        :return:
        """


class LessonTime:

    year = None
    term = None
    week = None
    day = None
    time = None
    datetime_string = None

    def __init__(self, _datetime = None, _datetime_string = None):
        # 初始化接受的参数为 datetime 类型或者一个我们自己定义的字符串
        if(_datetime):
            self.year = self.get_year(_datetime)
            self.term = self.get_term(_datetime)
            self.week = self.get_week(_datetime)
            self.day = self.get_day(_datetime)
            self.time = self.get_time(_datetime)
            self.datetime_string = '-'.join((str(self.year), str(self.term), str(self.week), str(self.day), str(self.time)))
        else:
            self.datetime_string = _datetime_string
            time_string = _datetime_string.split('-')
            self.year = time_string[0]
            self.term = time_string[1]
            self.week = time_string[2]
            self.day = time_string[3]
            self.time = time_string[4]

    @classmethod
    def from_string(cls, time_string):
        '''
        传入string类型的表示课的时间的字符串，格式为 '20152016-1-12-1-2'
        :param time_string: string
        :return:
        '''

        return cls


    @staticmethod
    def get_year(_datetime):
        if _datetime.month > 8:
            year = str(_datetime.year) + str(_datetime.year + 1)
        else:
            year = str(_datetime.year - 1) + str(_datetime.year)
        # year 格式为：20152016 字符串
        return year

    @staticmethod
    def get_term(_datetime):
        if _datetime.month in (9, 10, 11, 12, 1):
            term = 1
        else:
            term = 2
        return term

    @staticmethod
    def get_week(_datetime):
        if LessonTime.get_term(_datetime) == 1:
            return ((_datetime - startDayOfTheFirstTerm).days) // 7 + 1
        else:
            return ((_datetime - startDayOfTheSecondTerm).days) // 7 + 1

    @staticmethod
    def get_day(_datetime):
        return _datetime.weekday() + 1

    @staticmethod
    def get_time(_datetime):
        firstClassStartTime = datetime(_datetime.year, _datetime.month, _datetime.day, 8, 0)
        firstClassEndTime = datetime(_datetime.year, _datetime.month, _datetime.day, 9, 40)
        secondClassStartTime = datetime(_datetime.year, _datetime.month, _datetime.day, 10, 0)
        secondClassEndTime = datetime(_datetime.year, _datetime.month, _datetime.day, 11, 40)
        thirdClassStartTime = datetime(_datetime.year, _datetime.month, _datetime.day, 14, 30)
        thirdClassEndTime = datetime(_datetime.year, _datetime.month, _datetime.day, 16, 10)
        fourthClassStartTime = datetime(_datetime.year, _datetime.month, _datetime.day, 16, 30)
        fourthClassEndTime = datetime(_datetime.year, _datetime.month, _datetime.day, 18, 10)
        fifthClassStartTime = datetime(_datetime.year, _datetime.month, _datetime.day, 19, 0)
        fifthClassEndTime = datetime(_datetime.year, _datetime.month, _datetime.day, 20, 40)
        if firstClassStartTime < _datetime < firstClassEndTime:
            return 1
        if secondClassStartTime < _datetime < secondClassEndTime:
            return 2
        if thirdClassStartTime < _datetime < thirdClassEndTime:
            return 3
        if fourthClassStartTime < _datetime < fourthClassEndTime:
            return 4
        if fifthClassStartTime < _datetime < fifthClassEndTime:
            return 5
        return 0


class Course:

    name = None # 课程名称
    crs_id = None  # 课程id
    type = None # 课程类型，选修或必修

    # from_classroom_and_lessontime
    def __init__(self, classroom, lesson_time):
        sql = sql_getCourseByPositionAndTime
        with connection.cursor() as cursor:
            cursor.execute(sql, (classroom.clsrm_id, lesson_time.year, lesson_time.term, lesson_time.week, lesson_time.day, lesson_time.time))
            result = cursor.fetchone()
            self.name = result['name']
            self.crs_id = result['id']
            self.type = result['type']


class Lesson(Course, Classroom, LessonTime):
    """
    初始化时，clsrm_id和_position只用给一个, _datetime和_datetime_string只用给一个
    """
    def __init__(self, clsrm_id=None, _position=None, _datetime=None, _datetime_string=None):
        # 初始化 Classroom 父类
        if clsrm_id:
            Classroom.__init__(self, clsrm_id=clsrm_id)
        else:
            Classroom.__init__(self, _position=_position)

        # 初始化 LessonTime 父类
        if _datetime:
            LessonTime.__init__(self, _datetime = _datetime)
        else:
            LessonTime.__init__(self, _datetime_string = _datetime_string)

        # 初始化 Course 父类。这里由于 Course 类的构造函数使用的是 Classroom 和 LessonTime 的实例，所以这里就实例了一下
        if( _position):
            classroom = Classroom(_position=_position)
        else:
            classroom = Classroom(clsrm_id=clsrm_id)
        if( _datetime):
            lesson_time = LessonTime(_datetime = _datetime)
        else:
            lesson_time = LessonTime(_datetime_string=_datetime_string)
        Course.__init__(self, classroom, lesson_time)


    def __repr__(self):
        return '<Lesson %r, %r>' % (self.name, self._position)

    def nearby_lessons(self):
        # 获取这节课附近的教室
        positions = self.nearby_classrooms()
        lessons = []
        lesson = None
        for position in positions:
            #lesson = Lesson(clsrm_id=position.clsrm_id, _datetime_string=self.datetime_string)
            #lesson_copy = deepcopy(lesson)
            #lessons.append(lesson_copy)
            lessons.append(Lesson(clsrm_id=position.clsrm_id, _datetime_string=self.datetime_string))
            djfidjfidfj = 1213123
        return lessons

    @staticmethod
    def static_lessons(class_id):
        lessons = []
        sql = sql_getLessonsByClassId
        with connection.cursor() as cursor:
            cursor.execute(sql, class_id)
            results = cursor.fetchall()
            for result in results:
                datetime_string = "-".join([result['year'], result['term'], result['week'], result['day'], result['time']])
                lesson = Lesson(_position=result['position'],_datetime_string=datetime_string)
                lesson.fry_course_id = result['fry_course_id']  # 本来应该要让 Lesson 类再继承一个 Class 类的，但是没有些，所以关于class的属性就在这里临时加上了
                lesson.teacher_name = result['teacher_name']    # 同上，本来是要继承一个 Teacher 的，临时解决方案
                lessons.append(lesson)
            return lessons


class FryCourse:
    fry_course_id = None
    fry_course_name = None
    fry_course_teacher = None
    fry_course_schedule = []

    def __init__(self, fry_course_id=fry_course_id,fry_course_name=fry_course_name, fry_course_teacher=fry_course_teacher, fry_course_shedule=fry_course_schedule):
        self.fry_course_id = fry_course_id
        self.fry_course_name = fry_course_name
        self.fry_course_teacher = fry_course_teacher
        self.fry_course_schedule = fry_course_shedule

    @staticmethod
    def fry_course_by_fry_course_id(fry_course_id):
        '''接受一个 fry_course_id ，返回一个 fry_course 对象'''

        # 先通过给定的fry_course_id生成 lesson对象的序列
        sql = sql_get_lessons_by_fry_course_id
        with connection.cursor() as cursor:
            cursor.execute(sql, fry_course_id)
            results = cursor.fetchall()
        lessons = []
        for result in results:
            datetime_string = "-".join([result['year'], result['term'], result['week'], result['day'], result['time']])
            lesson = Lesson(clsrm_id=result['classroom_id'], _datetime_string=datetime_string)
            lesson.fry_course_id = result['fry_course_id']  # 本来应该要让 Lesson 类再继承一个 Class 类的，但是没有些，所以关于class的属性就在这里临时加上了
            lesson.teacher_name = result['teacher_name']    # 同上，本来是要继承一个 Teacher 的，临时解决方案
            lessons.append(lesson)

        # 将 lesson对象序列传给 静态方法 sing_fry_course，得到一门 course
        this_fry_course = FryCourse.single_fry_course(lessons)
        return this_fry_course

    @staticmethod
    def single_fry_course(single_lessons):
        '''
        返回一门 fry_course 类的对象
        传进来的 single_lessons 是一门 fry_course 的 lesson 的序列
        '''

        this_fry_course_id = single_lessons[0].fry_course_id
        this_fry_course_name = single_lessons[0].name
        this_fry_course_teacher = single_lessons[0].teacher_name
        this_fry_course_schedule = []
        for lesson in single_lessons:
            one_schedule = {}
            one_schedule['year'] = lesson.year
            one_schedule['term'] = lesson.term
            one_schedule['week'] = lesson.week
            one_schedule['weekday'] = lesson.day
            one_schedule['class_index'] = lesson.time
            one_schedule['campus'] = lesson.campus
            one_schedule['building'] = lesson.building
            one_schedule['floor'] = lesson.floor
            one_schedule['number'] = lesson.number
            one_schedule['position'] = lesson._position
            this_fry_course_schedule.append(one_schedule)
        # 最后返回的是单个的Fry_course对象
        return FryCourse(fry_course_id=this_fry_course_id, fry_course_name=this_fry_course_name,
                         fry_course_teacher=this_fry_course_teacher, fry_course_shedule=this_fry_course_schedule)

    @staticmethod
    def multiple_fry_courses(multiple_lessons):
        from itertools import tee
        #multiple_lessons, copy_multiple_lessons = tee(multiple_lessons) # 复制一份生成器用来遍历从而生成不用的class_id组成的列表
        from collections import defaultdict
        lessons_by_fry_course_id = defaultdict(list)
        for lesson in multiple_lessons:
            lesson_copy = deepcopy(lesson)
            lessons_by_fry_course_id[lesson_copy.fry_course_id].append(lesson_copy)
        fry_courses = []
        for fry_course_id in lessons_by_fry_course_id:
            fry_course = FryCourse.single_fry_course(lessons_by_fry_course_id[fry_course_id])
            fry_courses.append(fry_course)
        # 返回 Fry_course 对象的序列
        return fry_courses


class User:
    name = None

class Student(User):
    id = None
    password = None
    fry_courses_id = []

    def __init__(self, student_id):
        sql = sql_get_student
        with connection.cursor() as cursor:
            cursor.execute(sql, student_id)
            result = cursor.fetchone()
            if not result:
                return
        self.id = result['id']
        self.password = result['password']
        self.fry_courses_id = json.loads(result['mycourses'])
        pass

    def add_mycourse(self, fry_course_id=None, fry_course_obj=None):
        if fry_course_id:
            self.fry_courses_id.append(fry_course_id)
        else:
            self.fry_courses_id.append(fry_course_obj.fry_course_id)
        self.refresh_mycourse()

    def delete_mycourse(self, fry_course_id=None, fry_course_obj=None):
        if fry_course_id:
            self.fry_courses_id.remove(fry_course_id)
        else:
            self.fry_courses_id.remove(fry_course_obj.fry_course_id)
        self.refresh_mycourse()

    def refresh_mycourse(self):
        sql = sql_update_mycourse_to_student
        with connection.cursor() as cursor:
            re = cursor.execute(sql, (json.dumps(self.fry_courses_id), self.id))
        connection.commit()





class Teacher(User):
    pass

if __name__ == '__main__':
    #c = Classroom(_position = '六号楼6103')
    #t = LessonTime.from_string('20102011-1-1-3-1')
    #course = Course.from_classroom_and_lfry_courses = []


    #l = Lesson(_position='六号楼6103', _datetime_string='20102011-1-1-3-1')
    #nearby = l.nearby_lessons()
    ls = Lesson.static_lessons("2009003")
    fcs = FryCourse.multiple_fry_courses(ls)