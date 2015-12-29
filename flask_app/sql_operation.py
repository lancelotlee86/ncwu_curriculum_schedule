sql_getClassroomById = """
    SELECT *
    FROM classroom
    WHERE id = %s;"""

sql_getClassroomByPosition = """
    SELECT *
    FROM classroom
    WHERE position = %s;"""

#通过给定的 classroom id 返回与之相应的 position
sql_getPositionByClassroomId = """
	SELECT
		position
	FROM
		classroom
	WHERE
		id = %s
	"""

#通过给定的 position 返回与之相应的 classroom_id
sql_getClassroomIdByPosition = """
	SELECT
		id
	FROM
		classroom
	WHERE
		position = %s
	"""

# 通过给定的 class 返回这个班所有上的课
sql_getLessonsByClassId = """
SELECT
	*
FROM (
	SELECT
		*
	FROM (
		SELECT
			lesson.id,
			class.id AS 'class',
			class.major,
			lesson.fry_course_id,
			course.name AS 'course',
			lesson.year,
			lesson.term,
			lesson.week,
			lesson.day,
			lesson.time,
			classroom.position,
      lesson.teacher_id,
      teacher.name AS teacher_name
		FROM
			lesson inner join course inner join classroom inner join class INNER JOIN teacher
		WHERE
			class.id=lesson.class_id AND classroom.id=lesson.classroom_id AND course.id=lesson.course_id AND class.id=%s AND teacher.id=lesson.teacher_id
		) AS t
	WHERE t.day!='2' OR t.time!='4'
	) as tt
WHERE tt.day!='5' OR tt.time!='4'
"""

# 通过给定的教室position返回拥挤程度
sql_getCrowdednessRateByPosition = '''
    SELECT
        crowded_rate
    FROM
        crowdedness_record
    WHERE
        classroom_position = %s
    '''

# 通过给定的教室id返回拥挤程度
sql_getCrowdednessRateById = '''
    SELECT
        crowded_rate
    FROM
        crowdedness_record
    WHERE
        classroom_id = %s
    '''
"""
"""
# 通过给定的position返回相同楼层附近的教室position
sql_getNearbyPositionsByPosition = '''
    SELECT
        position
    FROM
        classroom
    WHERE
        (classroom.campus, classroom.building, classroom.floor) = (
                                                                        SELECT
                                                                            campus, building, floor
                                                                        FROM
                                                                            classroom
                                                                        WHERE
                                                                            classroom.position = %s
                                                                        )
    '''


"""
"""
# 通过给定的position和time返回这个position和time的课的course_name和position
sql_getCourseByPositionAndTime = '''
    SELECT
        course.name, course.id, course.type, alias_table.classroom_id
    FROM
        course JOIN (
                            SELECT
                                course_id, classroom_id
                            FROM
                                lesson
                            WHERE
                                lesson.classroom_id = %s AND lesson.year = %s AND lesson.term = %s AND lesson.week = %s AND lesson.day = %s AND lesson.time = %s
                            LIMIT 1
                        ) AS alias_table
    WHERE course.id = alias_table.course_id
    '''
"""
/* 通过给定的 username 返回密码*/
SELECT
	password
FROM
	student
WHERE
	id = 201315414
"""

sql_get_student = """
    SELECT * FROM student WHERE id=%s
"""

sql_update_mycourse_to_student = """
    UPDATE student SET mycourses = %s WHERE id=%s
"""