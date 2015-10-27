import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lishenzhi1214',
                             db='curriculum_schedule_app',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

#try:
    #with connection.cursor() as cursor:
        # Create a new record
        #sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        #cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    #connection.commit()

#    with connection.cursor() as cursor:
#        sql = "SELECT `id`, `position` FROM `classroom`"
#        cursor.execute(sql)
#        results = cursor.fetchall()
#        for result in results:
#            print(result)
        # Read a single record
        #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #cursor.execute(sql, ('webmaster@python.org',))
        #result = cursor.fetchone()
        #print(result)
#finally:
#    connection.close()


def func_getCrowdednessRateByPosition(position):
    sql = "SELECT crowded_rate FROM crowdedness_record WHERE classroom_position = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, position)
        result = cursor.fetchone()
        return result['crowded_rate']
