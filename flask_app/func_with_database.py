import pymysql.cursors
import time
from datetime import datetime
from flask_app.config import startDayOfTheFirstTerm, startDayOfTheSecondTerm
from flask_app.sql_operation import *
from flask_app.models import *

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lishenzhi1214',
                             db='curriculum_schedule_app',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)






def func_checkAccount(username, password):
    ''' 通过给定的账号密码验证是否符合数据库里存储的

    '''
    sql = "SELECT password FROM student WHERE id = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, username)
        result = cursor.fetchone()
        if password == result['password']:
            return True
        return False

def func_insertCrowdednessRateByPosition(rate, position):
    classroom_id = func_getClassroomIdByPosition(position)
    sql = 'INSERT INTO crowdedness_record (classroom_id, crowded_rate, timestamp) VALUES ( %s, %s, %s);'
    now = datetime.now()
    with connection.cursor() as cursor:
        cursor.execute(sql, (classroom_id, rate, now))
    return True

######################################################################################################
###################################### useless #####################################################
#####################################################################################################
def func_getNearbyPositionsByPosition(position):
    ''' 通过给定的position返回相同楼层附近的教室position

    '''
    classroom = Classroom(_position=position)
    positions = classroom.nearby_classrooms()
    classrooms = []
    for position in positions:
        c = Classroom(_position=position)
        classrooms.append(c)

def func_getPositionByClassroomId(classroom_id):
    ''' 通过给定的 classroom id 返回与之相应的 position

    '''
    sql = sql_getPositionByClassroomId

    with connection.cursor() as cursor:
        cursor.execute(sql, classroom_id)
        result = cursor.fetchone()
        return result['position']

def func_getClassroomIdByPosition(position):
    ''' 通过给定的 position 返回与之相应的 classroom_id

    '''
    sql = "SELECT id FROM classroom WHERE position = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, position)
        result = cursor.fetchone()
        return result['id']


def get_year(time):
    if(time.month > 8):
        year = str(time.year) + str(time.year + 1)
    else:
        year = str(time.year - 1) + str(time.year)
    # year 格式为：20152016 字符串
    return year

def get_term(time):
    if time.month in (9, 10, 11, 12, 1):
        term = 1
    else:
        term = 2
    return term

def get_week(time):
    if get_term(time) == 1:
        return ((time - startDayOfTheFirstTerm).days) // 7 + 1
    else:
        return ((time - startDayOfTheSecondTerm).days) // 7 + 1

def get_day(time):
    return time.weekday() + 1

def get_time(time):
    # now = datetime.now()
    # 下面的now都写错了，应该是time，这样子搞一下好了
    now = time
    firstClassStartTime = datetime(now.year, now.month, now.day, 8, 0)
    firstClassEndTime = datetime(now.year, now.month, now.day, 9, 40)
    secondClassStartTime = datetime(now.year, now.month, now.day, 10, 0)
    secondClassEndTime = datetime(now.year, now.month, now.day, 11, 40)
    thirdClassStartTime = datetime(now.year, now.month, now.day, 14, 30)
    thirdClassEndTime = datetime(now.year, now.month, now.day, 16, 10)
    fourthClassStartTime = datetime(now.year, now.month, now.day, 16, 30)
    fourthClassEndTime = datetime(now.year, now.month, now.day, 18, 10)
    fifthClassStartTime = datetime(now.year, now.month, now.day, 19, 0)
    fifthClassEndTime = datetime(now.year, now.month, now.day, 20, 40)
    if firstClassStartTime < time < firstClassEndTime:
        return 1
    if secondClassStartTime < time < secondClassEndTime:
        return 2
    if thirdClassStartTime < time < thirdClassEndTime:
        return 3
    if fourthClassStartTime < time < fourthClassEndTime:
        return 4
    if fifthClassStartTime < time < fifthClassEndTime:
        return 5

def func_getClassTimeByGivenTime(time):
    ''' 通过给定的 datetime.datetime 类型的 time 值，返回格式化后我们需要的 time

    '''

    year = get_year(time)
    term = get_term(time)
    week = get_week(time)
    day = get_day(time)
    time = get_time(time)
    classTime = [year, term, week, day, time]
    return classTime

def func_getCrowdednessRateByPosition(position):
    sql = "SELECT crowded_rate FROM crowdedness_record WHERE classroom_position = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, position)
        result = cursor.fetchone()
        return result['crowded_rate']

def func_getCourseNameAndPositionByTimeAndPosition(position, classTime):
    ''' 通过给定的position和time返回这个position和time的课的course_name和position还有classroom_id

    '''
    sql = "SELECT course.name, alias_table.classroom_id FROM course JOIN ( SELECT course_id, classroom_id FROM lesson WHERE lesson.classroom_id = %s AND lesson.year = %s AND lesson.term = %s AND lesson.week = %s AND lesson.day = %s AND lesson.time = %s LIMIT 1 ) AS alias_table WHERE course.id = alias_table.course_id"
    classroom_id = func_getClassroomIdByPosition(position)
    # 深度拷贝，参数传进来的classTime列表是传的引用
    classTime = classTime[:]
    classTime.insert(0, classroom_id)
    sqlParam = classTime

    with connection.cursor() as cursor:
        cursor.execute(sql, tuple(sqlParam))
        result = cursor.fetchone()
        if result:
            result['position'] = position
        # result = {'name': '自动控制原理', 'classroom_id': 1, 'position': '六号楼6302'}
        return result
