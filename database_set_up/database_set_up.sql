-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        10.0.19-MariaDB - mariadb.org binary distribution
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出 curriculum_schedule_app 的数据库结构
CREATE DATABASE IF NOT EXISTS `curriculum_schedule_app` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `curriculum_schedule_app`;


-- 导出  表 curriculum_schedule_app.class 结构
CREATE TABLE IF NOT EXISTS `class` (
  `id` int(11) NOT NULL,
  `major` varchar(50) NOT NULL,
  `department_id` int(11) DEFAULT NULL COMMENT '测试时是可以null的',
  PRIMARY KEY (`id`),
  KEY `FK_class_department` (`department_id`),
  CONSTRAINT `FK_class_department` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='班级表\r\nid：int 主键\r\nmajor：varchar、专业\r\ndepartment：varchar。学院';

-- 正在导出表  curriculum_schedule_app.class 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT IGNORE INTO `class` (`id`, `major`, `department_id`) VALUES
	(2013154, '计算机', 1),
	(2013155, '计算机', 1);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.classroom 结构
CREATE TABLE IF NOT EXISTS `classroom` (
  `id` int(11) NOT NULL,
  `campus` varchar(10) DEFAULT NULL,
  `building` varchar(10) DEFAULT NULL COMMENT '楼号',
  `floor` varchar(10) DEFAULT NULL COMMENT '层数',
  `number` varchar(10) DEFAULT NULL COMMENT '门牌号',
  `capacity` int(10) unsigned DEFAULT NULL,
  `classroom_number` varchar(10) NOT NULL COMMENT '测试用，稍后将数据拆分成3个字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='教室\r\nid: int 主键 教室id\r\nbuilding_number: varchar 楼号。如：No_1, No_2, No_S1 等\r\ncampus: varchar 校区。如：LongZiHu, HuaYuan\r\ncapacity: int 容量。';

-- 正在导出表  curriculum_schedule_app.classroom 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `classroom` DISABLE KEYS */;
INSERT IGNORE INTO `classroom` (`id`, `campus`, `building`, `floor`, `number`, `capacity`, `classroom_number`) VALUES
	(1, NULL, NULL, NULL, NULL, NULL, '龙4201');
/*!40000 ALTER TABLE `classroom` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.class_lesson 结构
CREATE TABLE IF NOT EXISTS `class_lesson` (
  `class_id` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  KEY `FK__lesson` (`lesson_id`),
  KEY `FK_class_lesson_class` (`class_id`),
  CONSTRAINT `FK__lesson` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`),
  CONSTRAINT `FK_class_lesson_class` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='班级要上的课时\r\nclass_id: int 外键指向class表主键id\r\nlesson_id: int 外键指向lesson表主键id';

-- 正在导出表  curriculum_schedule_app.class_lesson 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `class_lesson` DISABLE KEYS */;
INSERT IGNORE INTO `class_lesson` (`class_id`, `lesson_id`) VALUES
	(2013154, 1),
	(2013154, 2);
/*!40000 ALTER TABLE `class_lesson` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.course 结构
CREATE TABLE IF NOT EXISTS `course` (
  `id` int(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL COMMENT '测试时加上这个null',
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='课程\r\nname: 课程名称\r\ntype: 课程类型，有两个值供选择，选修为elective，必修为compulsory';

-- 正在导出表  curriculum_schedule_app.course 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT IGNORE INTO `course` (`id`, `type`, `name`) VALUES
	(1, NULL, '高等数学');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.crowdedness_record 结构
CREATE TABLE IF NOT EXISTS `crowdedness_record` (
  `id` int(11) NOT NULL,
  `classroom_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `crowded_rate` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_crowdedness_record_classroom` (`classroom_id`),
  CONSTRAINT `FK_crowdedness_record_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `classroom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='拥挤程度记录表\r\nid：int 主键。\r\nclassroom_id: int 外键指向classroom表主键id。教师id\r\ntimestamp：datetime。时间戳\r\ncrowded_rate: float 拥挤程度';

-- 正在导出表  curriculum_schedule_app.crowdedness_record 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `crowdedness_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `crowdedness_record` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.department 结构
CREATE TABLE IF NOT EXISTS `department` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学院\r\nid：int 主键\r\nname ：varchar 学院名称';

-- 正在导出表  curriculum_schedule_app.department 的数据：~1 rows (大约)
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT IGNORE INTO `department` (`id`, `name`) VALUES
	(1, '信息工程学院');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.lesson 结构
CREATE TABLE IF NOT EXISTS `lesson` (
  `id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `year` varchar(10) NOT NULL,
  `term` varchar(10) NOT NULL,
  `week` varchar(10) NOT NULL,
  `day` varchar(10) NOT NULL,
  `time` varchar(10) NOT NULL,
  `teacher_id` int(11) DEFAULT NULL COMMENT '测试时null',
  `classroom_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_lesson_course` (`course_id`),
  KEY `FK_lesson_classroom` (`classroom_id`),
  KEY `FK_lesson_teacher` (`teacher_id`),
  CONSTRAINT `FK_lesson_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `classroom` (`id`),
  CONSTRAINT `FK_lesson_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `FK_lesson_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='课时\r\nid: int 主键。\r\ncourse_id: int 外键，指向course表的主键id\r\nyear：varchar 。学年。如: "2014-2015", "2015-2016"\r\nterm: varchar. 学期。如："1", "2"\r\nweek: varchar. 周。如："1","17".\r\nday: varchar. 第几天。如："3", "7"\r\ntime: varchar 第几节。如："1","5"\r\nteacher_id: int, 外键，指向teacher表的主键id。任课教室id\r\nclassroom_id: int, 外键，指向classroom表的主键id。教室id';

-- 正在导出表  curriculum_schedule_app.lesson 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `lesson` DISABLE KEYS */;
INSERT IGNORE INTO `lesson` (`id`, `course_id`, `year`, `term`, `week`, `day`, `time`, `teacher_id`, `classroom_id`) VALUES
	(1, 1, '20102011', '1', '1', '1', '1', NULL, 1),
	(2, 1, '20102011', '1', '1', '2', '2', NULL, 1);
/*!40000 ALTER TABLE `lesson` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.student 结构
CREATE TABLE IF NOT EXISTS `student` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_student_class` (`class_id`),
  CONSTRAINT `FK_student_class` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学生\r\nid：int 主键\r\nname：varchar。姓名\r\npassword：varchar.密码\r\nclass_id: int 外键指向class表主键id';

-- 正在导出表  curriculum_schedule_app.student 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.student_lesson 结构
CREATE TABLE IF NOT EXISTS `student_lesson` (
  `student_id` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  KEY `FK_student_lesson_lesson` (`lesson_id`),
  KEY `FK_student_lesson_student` (`student_id`),
  CONSTRAINT `FK_student_lesson_lesson` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`),
  CONSTRAINT `FK_student_lesson_student` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学生要上的课时\r\nstudent_id int 外键指向student表主键id\r\nlesson_id int 外键指向lesson表主键id';

-- 正在导出表  curriculum_schedule_app.student_lesson 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `student_lesson` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_lesson` ENABLE KEYS */;


-- 导出  表 curriculum_schedule_app.teacher 结构
CREATE TABLE IF NOT EXISTS `teacher` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='教室\r\nid int 主键 教师id\r\nname varchar 教师姓名';

-- 正在导出表  curriculum_schedule_app.teacher 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
