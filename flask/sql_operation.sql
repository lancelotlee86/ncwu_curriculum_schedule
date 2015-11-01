/* 通过给定的 classroom id 返回与之相应的 position */
SELECT
	position
FROM
	classroom
WHERE
	id=1

/* 通过给定的 position 返回与之相应的 classroom_id */
SELECT
	id
FROM
	classroom
WHERE
	position = '六号楼6203'

/* 通过给定的 class 返回这个班所有上的课 */
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
			course.name AS 'course',
			lesson.year,
			lesson.term,
			lesson.week,
			lesson.day,
			lesson.time,
			classroom.position
		FROM
			lesson inner join course inner join classroom inner join class
		WHERE
			class.id=lesson.class_id AND classroom.id=lesson.classroom_id AND course.id=lesson.course_id AND class.id='2009003'
		) AS t
	WHERE t.day!='2' OR t.time!='4'
	) as tt
WHERE tt.day!='5' OR tt.time!='4'


/* 通过给定的教室position返回拥挤程度 */
SELECT
	crowded_rate
FROM
	crowdedness_record
WHERE
	classroom_position = '六号楼6202'


/* 通过给定的position返回相同楼层附近的教室position */
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
    																	classroom.position = '六号楼6302'
    																)


/* 通过给定的position和time返回这个position和time的课的course_name和position */
SELECT
	course.name, alias_table.classroom_id
FROM
	course JOIN (
						SELECT
							course_id, classroom_id
						FROM
							lesson
						WHERE
							lesson.classroom_id = 1 AND lesson.year = 20102011 AND lesson.term = 1 AND lesson.week = 9 AND lesson.day = 1 AND lesson.time = 1
						LIMIT 1
					) AS alias_table
WHERE course.id = alias_table.course_id

/* 通过给定的 username 返回密码*/
SELECT
	password
FROM
	student
WHERE
	id = 201315414
