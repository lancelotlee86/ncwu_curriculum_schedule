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
