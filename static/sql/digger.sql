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