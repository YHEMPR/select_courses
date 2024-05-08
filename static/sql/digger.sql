DELIMITER $$

CREATE TRIGGER BeforeInsertStudent
BEFORE INSERT ON student
FOR EACH ROW
BEGIN
    -- 检查dept_id是否存在于department表中
    IF NOT EXISTS (SELECT 1 FROM department WHERE dept_id = NEW.dept_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '院系号不存在';
    END IF;

    -- 检查性别是否为“男”或“女”
    IF NEW.sex NOT IN ('男', '女') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '性别只能为男或女';
    END IF;

    -- 检查状态是否为“在校”或“毕业”
    IF NEW.Status NOT IN ('在校', '毕业') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '状态只能为在校或毕业';
    END IF;

    -- 检查手机号码格式（假设必须有11位）
    IF CHAR_LENGTH(NEW.mobile_phone) != 11 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '手机号码格式不正确';
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER BeforeUpdateStudent
BEFORE UPDATE ON student
FOR EACH ROW
BEGIN
    -- 确保学号未被更改
    IF OLD.student_id != NEW.student_id THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '学号不能修改';
    END IF;

    -- 检查dept_id是否存在于department表中
    IF NOT EXISTS (SELECT 1 FROM department WHERE dept_id = NEW.dept_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '院系号不存在';
    END IF;

    -- 检查性别是否为“男”或“女”
    IF NEW.sex NOT IN ('男', '女') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '性别只能为男或女';
    END IF;

    -- 检查状态是否为“在校”或“毕业”
    IF NEW.Status NOT IN ('在校', '毕业') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '状态只能为在校或毕业';
    END IF;

    -- 检查手机号码格式（假设必须有11位）
    IF CHAR_LENGTH(NEW.mobile_phone) != 11 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '手机号码格式不正确';
    END IF;
END$$

DELIMITER ;


-- 创建插入前触发器
DELIMITER $$
CREATE TRIGGER `BeforeInsertTeacher` BEFORE INSERT ON `teacher` FOR EACH ROW
BEGIN
    IF NEW.sex NOT IN ('男', '女') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '性别只能是男或女';
    END IF;
    IF NEW.professional_ranks NOT IN ('副教授', '讲师', '教授', '助教') OR NEW.professional_ranks IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '职称必须是副教授、讲师、教授或助教之一';
    END IF;
    IF NEW.salary <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '工资必须为正值';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM department WHERE dept_id = NEW.dept_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '院系编号不存在';
    END IF;
END$$
DELIMITER ;

-- 创建更新前触发器
DELIMITER $$
CREATE TRIGGER `BeforeUpdateTeacher` BEFORE UPDATE ON `teacher` FOR EACH ROW
BEGIN
    IF NEW.sex NOT IN ('男', '女') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '性别只能是男或女';
    END IF;
    IF NEW.professional_ranks NOT IN ('副教授', '讲师', '教授', '助教') OR NEW.professional_ranks IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '职称必须是副教授、讲师、教授或助教之一';
    END IF;
    IF NEW.salary <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '工资必须为正值';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM department WHERE dept_id = NEW.dept_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '院系编号不存在';
    END IF;
END$$
DELIMITER ;

# 成绩触发器
DELIMITER $$

CREATE TRIGGER prevent_lower_score
BEFORE INSERT ON course_selection
FOR EACH ROW
BEGIN
    DECLARE prev_score VARCHAR(3);

    -- 获取之前的成绩
    SELECT score INTO prev_score
    FROM course_selection
    WHERE student_id = NEW.student_id
    AND course_id = NEW.course_id;

    -- 如果之前的成绩存在且新成绩低于之前的成绩，则阻止插入操作
    IF prev_score IS NOT NULL AND NEW.score < prev_score THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '新成绩不能低于之前的成绩';
    END IF;
END;
$$

DELIMITER ;


# 课程表触发器
DELIMITER $$

CREATE TRIGGER BeforeInsertCourse
BEFORE INSERT ON course
FOR EACH ROW
BEGIN
    -- 检查课名是否为空
    IF NEW.course_name IS NULL OR NEW.course_name = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '课程名称不能为空';
    END IF;

    -- 检查学分是否为正数
    IF NEW.credit IS NULL OR NEW.credit <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '学分必须是正数';
    END IF;

    -- 检查学时是否为正数
    IF NEW.credit_hours IS NULL OR NEW.credit_hours <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '学时必须是正数';
    END IF;

    -- 检查院系号是否存在于department表中
    DECLARE dept_count INT;
    SELECT COUNT(*) INTO dept_count FROM department WHERE dept_id = NEW.dept_id;
    IF dept_count = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '院系编号不存在';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER BeforeUpdateCourse
BEFORE UPDATE ON course
FOR EACH ROW
BEGIN
    -- 检查课名是否为空
    IF NEW.course_name IS NULL OR NEW.course_name = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '课程名称不能为空';
    END IF;

    -- 检查学分是否为正数
    IF NEW.credit IS NULL OR NEW.credit <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '学分必须是正数';
    END IF;

    -- 检查学时是否为正数
    IF NEW.credit_hours IS NULL OR NEW.credit_hours <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '学时必须是正数';
    END IF;

    -- 检查院系号是否存在于department表中
    SET @dept_count = (SELECT COUNT(*) FROM department WHERE dept_id = NEW.dept_id);
    IF @dept_count = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '院系编号不存在';
    END IF;
END$$

DELIMITER ;


# 成绩触发器不能为负，且不能低于前值,0-100
DELIMITER $$

CREATE TRIGGER BeforeUpdateCourseSelectionScore
BEFORE UPDATE ON course_selection
FOR EACH ROW
BEGIN
    -- 检查成绩是否超过100或小于0
    IF NEW.score > 100 OR NEW.score < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '成绩必须在0到100分之间';
    END IF;

    -- 检查更新的成绩是否低于之前的成绩
    IF NEW.score < OLD.score THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '新的成绩不能低于旧的成绩';
    END IF;
END$$

DELIMITER ;
