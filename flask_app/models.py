from flask import Flask
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

    _id = None
    campus = None
    building = None
    floor = None
    number = None
    capacity = None
    _position = None

    def __init__(self, _id=None, _position=None):
        if(_id):
            sql = sql_getClassroomById
        elif(_position):
            sql = sql_getClassroomByPosition
        else:
            sql = ''
        with connection.cursor() as cursor:
            cursor.execute(sql, _id if _id else _position)
            result = cursor.fetchone()
            self._id = result['id']
            self.campus = result['campus']
            self.building = result['building']
            self.floor = result['floor']
            self.number = result['capacity']
            self._position = result['position']

    def __repr__(self):
        return '<Classroom %r>' % self._position

    def get_nearby_classrooms(self):
        '''
        返回当前对象代表教室的附近所有的教室, 返回的是对象列表
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
            cursor.execute(sql, self._id)
            result = cursor.fetchone()
            return result


class LessonTime:

    year = None
    term = None
    week = None
    day = None
    time = None

    def __init__(self, _datetime):
        self.year = self.get_year(_datetime)
        self.term = self.get_term(_datetime)
        self.week = self.get_week(_datetime)
        self.day = self.get_day(_datetime)
        self.time = self.get_time(_datetime)

    @classmethod
    def from_string(cls, time_string):
        '''
        传入string类型的表示课的时间的字符串，格式为 '20152016-1-12-1-2'
        :param time_string: string
        :return:
        '''
        time_string = time_string.split('-')
        cls.year = time_string[0]
        ###################################################################


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
    _id = None  # 课程id
    type = None # 课程类型，选修或必修

    # def __init__(self, ):


    @classmethod
    def from_classroom_and_lessontime(cls, classroom, lesson_time):
        sql = sql_getCourseByPositionAndTime
        with connection.cursor() as cursor:
            cursor.execute(sql, (classroom._id, lesson_time.year, lesson_time.term, lesson_time.week, lesson_time.day, lesson_time.time))
            result = cursor.fetchone()




if __name__ == '__main__':
    c = Classroom(_position = '六号楼6103')
    cs = c.get_nearby_classrooms()
    c.crowdedness()

