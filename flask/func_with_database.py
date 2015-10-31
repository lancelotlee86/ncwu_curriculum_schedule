import pymysql.cursors
import time
from datetime import datetime
from config import startDayOfTheFirstTerm, startDayOfTheSecondTerm

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lishenzhi1214',
                             db='curriculum_schedule_app',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


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
    today = datetime.today()
    if get_term(time) == 1:
        return ((today - startDayOfTheFirstTerm).days) // 7 + 1
    else:
        return ((today - startDayOfTheSecondTerm).days) // 7 + 1

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


def func_getPositionByClassroomId(classroom_id):
    ''' 通过给定的 classroom id 返回与之相应的 position

    '''
    sql = "SELECT position FROM classroom WHERE id = %s"

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

def func_getCrowdednessRateByPosition(position):
    sql = "SELECT crowded_rate FROM crowdedness_record WHERE classroom_position = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, position)
        result = cursor.fetchone()
        return result['crowded_rate']

def func_getNearbyPositionByPosition(position):
    ''' 通过给定的position返回相同楼层附近的教室position

    '''
    sql = "SELECT position FROM classroom WHERE (classroom.campus, classroom.building, classroom.floor) = (SELECT campus, building, floor FROM classroom WHERE classroom.position = %s)"

    with connection.cursor() as cursor:
        cursor.execute(sql, position)
        results = cursor.fetchall()
        # results 现在是一个字典列表，是这样的：[{'position': '六号楼6303'}, {'position': '六号楼6304'}, {'position': '六号楼6302'}]
        #下面将其转换为简单的列表
        positions = []
        for result in results:
            positions.append(result['position'])
        # 现在的positions是这样的：['六号楼6303', '六号楼6304', '六号楼6302']
        return positions

def func_getCourseNameAndPositionByTimeAndPosition(position, classTime):
    ''' 通过给定的position和time返回这个position和time的课的course_name和position还有classroom_id

    '''
    sql = "SELECT course.name, alias_table.classroom_id FROM course JOIN ( SELECT course_id, classroom_id FROM lesson WHERE lesson.classroom_id = %s AND lesson.year = %s AND lesson.term = %s AND lesson.week = %s AND lesson.day = %s AND lesson.time = %s LIMIT 1 ) AS alias_table WHERE course.id = alias_table.course_id"
    classroom_id = func_getClassroomIdByPosition(position)
    classTime.insert(0, classroom_id)
    sqlParam = classTime

    with connection.cursor() as cursor:
        cursor.execute(sql, tuple(sqlParam))
        result = cursor.fetchone()
        result['position'] = position
        # result = {'name': '自动控制原理', 'classroom_id': 1, 'position': '六号楼6302'}
        return result
