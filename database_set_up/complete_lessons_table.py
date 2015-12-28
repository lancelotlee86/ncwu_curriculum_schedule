import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lishenzhi1214',
                             db='curriculum_schedule_app',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def add_info():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM lesson"
        cursor.execute(sql)
        results = cursor.fetchall()
    for result in results:
        if result['id']%1000 == 0:
            print(result['id'])
        with connection.cursor() as cursor1:
            sql = "UPDATE lesson SET fry_course_id = %s WHERE id = %s;"
            cursor1.execute(sql, (str(result['course_id']) + str(result['class_id']), int(result['id'] )))
            connection.commit()


if __name__ == '__main__':
    add_info()
