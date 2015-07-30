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
  `id` varchar(11) NOT NULL,
  `major` varchar(50) NOT NULL,
  `department_id` varchar(11) DEFAULT NULL COMMENT '测试时是可以null的',
  PRIMARY KEY (`id`),
  KEY `FK_class_department` (`department_id`),
  CONSTRAINT `FK_class_department` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='班级表\r\nid：int 主键\r\nmajor：varchar、专业\r\ndepartment：varchar。学院';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.classroom 结构
CREATE TABLE IF NOT EXISTS `classroom` (
  `id` int(11) NOT NULL COMMENT '自增，没什么意义',
  `campus` varchar(10) DEFAULT NULL,
  `building` varchar(10) DEFAULT NULL COMMENT '楼号',
  `floor` varchar(10) DEFAULT NULL COMMENT '层数',
  `number` varchar(10) DEFAULT NULL COMMENT '门牌号',
  `capacity` int(10) unsigned DEFAULT NULL,
  `position` varchar(10) DEFAULT NULL COMMENT '测试用，稍后将数据拆分成3个字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='教室\r\nid: int 主键 教室id\r\nbuilding_number: varchar 楼号。如：No_1, No_2, No_S1 等\r\ncampus: varchar 校区。如：LongZiHu, HuaYuan\r\ncapacity: int 容量。';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.class_lesson 结构
CREATE TABLE IF NOT EXISTS `class_lesson` (
  `lesson_id` int(11) DEFAULT NULL,
  `class_id` varchar(11) DEFAULT NULL,
  KEY `FK_class_lesson_lesson` (`lesson_id`),
  KEY `FK_class_lesson_class` (`class_id`),
  CONSTRAINT `FK_class_lesson_class` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`),
  CONSTRAINT `FK_class_lesson_lesson` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.course 结构
CREATE TABLE IF NOT EXISTS `course` (
  `id` varchar(11) NOT NULL,
  `type` varchar(50) DEFAULT NULL COMMENT '测试时加上这个null',
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='课程\r\nname: 课程名称\r\ntype: 课程类型，有两个值供选择，选修为elective，必修为compulsory';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.crowdedness_record 结构
CREATE TABLE IF NOT EXISTS `crowdedness_record` (
  `id` int(11) NOT NULL COMMENT '自增，没有意义',
  `classroom_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `crowded_rate` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_crowdedness_record_classroom` (`classroom_id`),
  CONSTRAINT `FK_crowdedness_record_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `classroom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='拥挤程度记录表\r\nid：int 主键。\r\nclassroom_id: int 外键指向classroom表主键id。教师id\r\ntimestamp：datetime。时间戳\r\ncrowded_rate: float 拥挤程度';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.department 结构
CREATE TABLE IF NOT EXISTS `department` (
  `id` varchar(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学院\r\nid：int 主键\r\nname ：varchar 学院名称';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.lesson 结构
CREATE TABLE IF NOT EXISTS `lesson` (
  `id` int(11) NOT NULL,
  `course_id` varchar(11) NOT NULL,
  `class_id` varchar(11) NOT NULL,
  `year` varchar(10) NOT NULL,
  `term` varchar(10) NOT NULL,
  `week` varchar(10) NOT NULL,
  `day` varchar(10) NOT NULL,
  `time` varchar(10) NOT NULL,
  `teacher_id` varchar(11) DEFAULT NULL COMMENT '测试时null',
  `classroom_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_lesson_classroom` (`classroom_id`),
  KEY `FK_lesson_course` (`course_id`),
  KEY `FK_lesson_teacher` (`teacher_id`),
  KEY `FK_lesson_class` (`class_id`),
  CONSTRAINT `FK_lesson_class` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`),
  CONSTRAINT `FK_lesson_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `classroom` (`id`),
  CONSTRAINT `FK_lesson_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `FK_lesson_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='课时\r\nid: int 主键。\r\ncourse_id: int 外键，指向course表的主键id\r\nyear：varchar 。学年。如: "2014-2015", "2015-2016"\r\nterm: varchar. 学期。如："1", "2"\r\nweek: varchar. 周。如："1","17".\r\nday: varchar. 第几天。如："3", "7"\r\ntime: varchar 第几节。如："1","5"\r\nteacher_id: int, 外键，指向teacher表的主键id。任课教室id\r\nclassroom_id: int, 外键，指向classroom表的主键id。教室id';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.student 结构
CREATE TABLE IF NOT EXISTS `student` (
  `id` varchar(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `class_id` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_student_class` (`class_id`),
  CONSTRAINT `FK_student_class` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学生\r\nid：int 主键\r\nname：varchar。姓名\r\npassword：varchar.密码\r\nclass_id: int 外键指向class表主键id';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.student_lesson 结构
CREATE TABLE IF NOT EXISTS `student_lesson` (
  `student_id` varchar(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  KEY `FK_student_lesson_student` (`student_id`),
  KEY `FK_student_lesson_lesson` (`lesson_id`),
  CONSTRAINT `FK_student_lesson_lesson` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`),
  CONSTRAINT `FK_student_lesson_student` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学生要上的课时\r\nstudent_id int 外键指向student表主键id\r\nlesson_id int 外键指向lesson表主键id';

-- 数据导出被取消选择。


-- 导出  表 curriculum_schedule_app.teacher 结构
CREATE TABLE IF NOT EXISTS `teacher` (
  `id` varchar(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='教室\r\nid int 主键 教师id\r\nname varchar 教师姓名';

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
