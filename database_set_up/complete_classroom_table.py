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
        sql = "SELECT * FROM classroom"
        cursor.execute(sql)
        results = cursor.fetchall()
    for result in results:
        if result['campus'] == '花园校区' or ('美术工作室' in result['position']) or result['position'] == '':
            continue
        position = result['position']
        with connection.cursor() as cursor1:
            sql = "UPDATE classroom SET building = %s, floor = %s, number = %s WHERE position = %s;"
            cursor1.execute(sql, (position[-4], position[-3], str(int(position[-2:])), position))
            connection.commit()


if __name__ == '__main__':
    add_info()
