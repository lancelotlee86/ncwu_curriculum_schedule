import pymysql.cursors
from datetime import datetime
from flask_app.sql_operation import *
from flask_app.config import startDayOfTheFirstTerm, startDayOfTheSecondTerm

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
        sql = sql_getCrowdednessRateById
        with connection.cursor() as cursor:
            cursor.execute(sql, self.clsrm_id)
            result = cursor.fetchone()
            return result


class LessonTime:

    year = None
    term = None
    week = None
    day = None
    time = None
    datetime_string = None

    def __init__(self, _datetime):
        # 初始化接受的参数为 datetime 类型
        self.year = self.get_year(_datetime)
        self.term = self.get_term(_datetime)
        self.week = self.get_week(_datetime)
        self.day = self.get_day(_datetime)
        self.time = self.get_time(_datetime)
        self.datetime_string = '-'.join((str(self.year), str(self.term), str(self.week), str(self.day), str(self.time)))

    @classmethod
    def from_string(cls, time_string):
        '''
        传入string类型的表示课的时间的字符串，格式为 '20152016-1-12-1-2'
        :param time_string: string
        :return:
        '''
        cls.datetime_string = time_string
        time_string = time_string.split('-')
        cls.year = time_string[0]
        cls.term = time_string[1]
        cls.week = time_string[2]
        cls.day = time_string[3]
        cls.time = time_string[4]
        return cls


    @staticmethod
    def get_year(_datetime):
        if(_datetime.month > 8):
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

    # def __init__(self, )
    @classmethod
    def from_classroom_and_lessontime(cls, classroom, lesson_time):
        sql = sql_getCourseByPositionAndTime
        with connection.cursor() as cursor:
            cursor.execute(sql, (classroom.clsrm_id, lesson_time.year, lesson_time.term, lesson_time.week, lesson_time.day, lesson_time.time))
            result = cursor.fetchone()
            cls.name = result['name']
            cls.crs_id = result['id']
            cls.type = result['type']
        return cls


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
            LessonTime.__init__(self, _datetime)
        else:
            LessonTime.from_string(_datetime_string)

        # 初始化 Course 父类。这里由于 Course 类的构造函数使用的是 Classroom 和 LessonTime 的实例，所以这里就实例了一下
        if( _position):
            classroom = Classroom(_position=_position)
        else:
            classroom = Classroom(clsrm_id=clsrm_id)
        if( _datetime):
            lesson = LessonTime(_datetime)
        else:
            lesson = LessonTime.from_string(_datetime_string)
        Course.from_classroom_and_lessontime(classroom, lesson)

    def __repr__(self):
        return '<Lesson %r, %r>' % (self.name, self._position)

    def nearby_lessons(self):
        # 获取这节课附近的教室
        positions = self.nearby_classrooms()
        lessons = []
        for position in positions:
            lesson = Lesson(clsrm_id=position.clsrm_id, _datetime_string=self.datetime_string)
            lessons.append(lesson)
        return lessons


if __name__ == '__main__':
    #c = Classroom(_position = '六号楼6103')
    #t = LessonTime.from_string('20102011-1-1-3-1')
    #course = Course.from_classroom_and_lessontime(c, t)

    lesson = Lesson(_position='六号楼6103', _datetime_string='20102011-1-1-3-1')


