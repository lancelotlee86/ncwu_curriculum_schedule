import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lishenzhi1214',
                             db='curriculum_schedule_app',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



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

def func_getCourseNameAndPositionByTimeAndPosition(position, year, term, week, day, time):
    ''' 通过给定的position和time返回这个position和time的课的course_name和position还有classroom_id

    '''
    sql = "SELECT course.name, alias_table.classroom_id FROM course JOIN ( SELECT course_id, classroom_id FROM lesson WHERE lesson.classroom_id = %s AND lesson.year = %s AND lesson.term = %s AND lesson.week = %s AND lesson.day = %s AND lesson.time = %s LIMIT 1 ) AS alias_table WHERE course.id = alias_table.course_id"
    classroom_id = func_getClassroomIdByPosition(position)

    with connection.cursor() as cursor:
        cursor.execute(sql, (classroom_id, year, term, week, day, time))
        result = cursor.fetchone()
        result['position'] = position
        # result = {'name': '自动控制原理', 'classroom_id': 1, 'position': '六号楼6302'}
        return result
