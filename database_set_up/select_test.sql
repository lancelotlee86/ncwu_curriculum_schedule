SELECT
	lesson.id,
	class.id AS 'class_id',
	class.major,
	course.name AS 'course_name',
	lesson.year,
	lesson.term,
	lesson.week,
	lesson.day,
	lesson.time,
	classroom.classroom_number
FROM 
	lesson inner join class_lesson inner join course inner join classroom inner join class inner join department
WHERE
	class.id=class_lesson.class_id AND class_lesson.lesson_id=lesson.id AND class.id='2013154';