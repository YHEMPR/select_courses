/*
 Navicat Premium Data Transfer

 Source Server         : yhempr
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3306
 Source Schema         : school

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 25/04/2024 13:28:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class`  (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `semester` char(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '学期',
  `course_id` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课号',
  `staff_id` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工号',
  `class_time` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '上课时间',
  PRIMARY KEY (`class_id`) USING BTREE,
  UNIQUE INDEX `course_id`(`course_id` ASC, `staff_id` ASC) USING BTREE,
  INDEX `fk_class_teacher`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `fk_class_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_class_teacher` FOREIGN KEY (`staff_id`) REFERENCES `teacher` (`staff_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 206 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '开课表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of class
-- ----------------------------
INSERT INTO `class` VALUES (1, '201302', '08302001', '0201', '星期一5-8');
INSERT INTO `class` VALUES (2, '202301', '08302002', '0202', '星期三1-4');
INSERT INTO `class` VALUES (3, '202301', '08302003', '0202', '星期四1-4');
INSERT INTO `class` VALUES (4, '202301', '08302004', '0203', '星期五1-4');
INSERT INTO `class` VALUES (5, '201301', '08305001', '0102', '星期一5-8');
INSERT INTO `class` VALUES (6, '201201', '08305001', '0103', '星期三5-8');
INSERT INTO `class` VALUES (7, '201202', '08305002', '0101', '星期三1-4');
INSERT INTO `class` VALUES (8, '201202', '08305002', '0102', '星期三1-4');
INSERT INTO `class` VALUES (9, '201202', '08305002', '0103', '星期三1-4');
INSERT INTO `class` VALUES (10, '201202', '08305003', '0102', '星期五5-8');
INSERT INTO `class` VALUES (11, '201301', '08305004', '0101', '星期二1-4');
INSERT INTO `class` VALUES (12, '201302', '08301001', '0210', '星期一5-8');
INSERT INTO `class` VALUES (13, '202302', '08302009', '0211', '星期一1-4');
INSERT INTO `class` VALUES (14, '202302', '08302010', '0212', '星期二1-4');
INSERT INTO `class` VALUES (15, '202302', '08302011', '0213', '星期三1-4');
INSERT INTO `class` VALUES (16, '202302', '08302012', '0214', '星期四1-4');
INSERT INTO `class` VALUES (17, '202302', '08302013', '0215', '星期五1-4');
INSERT INTO `class` VALUES (18, '202302', '08302014', '0216', '星期一1-4');
INSERT INTO `class` VALUES (19, '202302', '08302015', '0217', '星期二1-4');
INSERT INTO `class` VALUES (20, '202302', '08302016', '0218', '星期三1-4');
INSERT INTO `class` VALUES (21, '202302', '08302017', '0219', '星期四1-4');
INSERT INTO `class` VALUES (22, '202302', '08302018', '0220', '星期五1-4');
INSERT INTO `class` VALUES (186, '202401', '08306001', '0221', '星期三1-4');
INSERT INTO `class` VALUES (187, '202401', '08306002', '0222', '星期四1-4');
INSERT INTO `class` VALUES (188, '202401', '08306003', '0223', '星期五1-4');
INSERT INTO `class` VALUES (189, '202401', '08306004', '0213', '星期一1-4');
INSERT INTO `class` VALUES (190, '202401', '08306005', '0213', '星期二1-4');
INSERT INTO `class` VALUES (191, '202401', '08306006', '0213', '星期三1-4');
INSERT INTO `class` VALUES (192, '202401', '08306007', '0214', '星期四1-4');
INSERT INTO `class` VALUES (193, '202401', '08306008', '0214', '星期五1-4');
INSERT INTO `class` VALUES (194, '202401', '08306009', '0215', '星期一1-4');
INSERT INTO `class` VALUES (195, '202401', '08306010', '0215', '星期二1-4');
INSERT INTO `class` VALUES (196, '202401', '08306011', '0221', '星期三1-4');
INSERT INTO `class` VALUES (197, '202401', '08306012', '0222', '星期四1-4');
INSERT INTO `class` VALUES (198, '202401', '08306013', '0223', '星期五1-4');
INSERT INTO `class` VALUES (199, '202401', '08306014', '0234', '星期一1-4');
INSERT INTO `class` VALUES (200, '202401', '08306015', '0234', '星期二1-4');
INSERT INTO `class` VALUES (201, '202401', '08306016', '0234', '星期三1-4');
INSERT INTO `class` VALUES (202, '202401', '08306017', '0235', '星期四1-4');
INSERT INTO `class` VALUES (203, '202401', '08306018', '0235', '星期五1-4');
INSERT INTO `class` VALUES (204, '202401', '08306019', '0236', '星期一1-4');
INSERT INTO `class` VALUES (205, '202401', '08306020', '0236', '星期二1-4');

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `course_id` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课号',
  `course_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '课名',
  `credit` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学分',
  `credit_hours` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学时',
  `dept_id` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '院系号',
  PRIMARY KEY (`course_id`) USING BTREE,
  INDEX `idx2`(`course_name` ASC) USING BTREE,
  INDEX `course_dept_fk`(`dept_id` ASC) USING BTREE,
  CONSTRAINT `course_dept_fk` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '课程表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES ('08301001', '分子物理学', '4', '40', '03');
INSERT INTO `course` VALUES ('08301002', '材料力学', '3', '30', '03');
INSERT INTO `course` VALUES ('08301003', '材料物理学', '3', '30', '03');
INSERT INTO `course` VALUES ('08301004', '材料化学', '3', '30', '03');
INSERT INTO `course` VALUES ('08302001', '通信学', '3', '30', '02');
INSERT INTO `course` VALUES ('08302002', '计算机网络', '4', '40', '01');
INSERT INTO `course` VALUES ('08302003', '人工智能', '4', '40', '01');
INSERT INTO `course` VALUES ('08302004', '操作系统', '4', '40', '01');
INSERT INTO `course` VALUES ('08302005', '软件工程', '4', '40', '01');
INSERT INTO `course` VALUES ('08302006', '算法设计', '4', '40', '01');
INSERT INTO `course` VALUES ('08302007', '数据挖掘', '4', '40', '01');
INSERT INTO `course` VALUES ('08302008', '人机交互', '4', '40', '01');
INSERT INTO `course` VALUES ('08302009', '计算机组成原理', '4', '40', '01');
INSERT INTO `course` VALUES ('08302010', '软件工程', '4', '40', '01');
INSERT INTO `course` VALUES ('08302011', '人机交互', '4', '40', '01');
INSERT INTO `course` VALUES ('08302012', '网络编程', '4', '40', '01');
INSERT INTO `course` VALUES ('08302013', '移动应用开发', '4', '40', '01');
INSERT INTO `course` VALUES ('08302014', '信息安全', '4', '40', '01');
INSERT INTO `course` VALUES ('08302015', '人工智能', '4', '40', '01');
INSERT INTO `course` VALUES ('08302016', '大数据技术', '4', '40', '01');
INSERT INTO `course` VALUES ('08302017', '云计算', '4', '40', '01');
INSERT INTO `course` VALUES ('08302018', '物联网技术', '4', '40', '01');
INSERT INTO `course` VALUES ('08302019', '区块链技术', '4', '40', '01');
INSERT INTO `course` VALUES ('08302020', '机器学习', '4', '40', '01');
INSERT INTO `course` VALUES ('08305001', '离散数学', '4', '40', '01');
INSERT INTO `course` VALUES ('08305002', '数据库原理', '4', '50', '01');
INSERT INTO `course` VALUES ('08305003', '数据结构', '4', '50', '01');
INSERT INTO `course` VALUES ('08305004', '系统结构', '6', '60', '01');
INSERT INTO `course` VALUES ('08305005', '编程语言', '4', '40', '01');
INSERT INTO `course` VALUES ('08305006', '网络安全', '4', '40', '01');
INSERT INTO `course` VALUES ('08305007', '信息检索', '4', '40', '01');
INSERT INTO `course` VALUES ('08305008', '大数据处理', '4', '40', '01');
INSERT INTO `course` VALUES ('08305009', '计算理论', '4', '40', '01');
INSERT INTO `course` VALUES ('08305010', '分布式系统', '4', '40', '01');
INSERT INTO `course` VALUES ('08305011', '软件测试', '4', '40', '01');
INSERT INTO `course` VALUES ('08305012', '操作系统原理', '4', '40', '01');
INSERT INTO `course` VALUES ('08305013', '计算机图形学', '4', '40', '01');
INSERT INTO `course` VALUES ('08305014', '并行计算', '4', '40', '01');
INSERT INTO `course` VALUES ('08305015', '嵌入式系统', '4', '40', '01');
INSERT INTO `course` VALUES ('08305016', '云计算', '4', '40', '01');
INSERT INTO `course` VALUES ('08305017', '人工智能原理', '4', '40', '01');
INSERT INTO `course` VALUES ('08306001', '文学概论', '3', '30', '09');
INSERT INTO `course` VALUES ('08306002', '西方文化史', '3', '30', '09');
INSERT INTO `course` VALUES ('08306003', '中国文学史', '3', '30', '09');
INSERT INTO `course` VALUES ('08306004', '经济学原理', '4', '40', '04');
INSERT INTO `course` VALUES ('08306005', '国际贸易', '4', '40', '04');
INSERT INTO `course` VALUES ('08306006', '宏观经济学', '4', '40', '04');
INSERT INTO `course` VALUES ('08306007', '英语语法', '3', '30', '05');
INSERT INTO `course` VALUES ('08306008', '英美文学选读', '3', '30', '05');
INSERT INTO `course` VALUES ('08306009', '外交学', '4', '40', '05');
INSERT INTO `course` VALUES ('08306010', '国际关系概论', '3', '30', '05');
INSERT INTO `course` VALUES ('08306011', '世界历史', '3', '30', '09');
INSERT INTO `course` VALUES ('08306012', '中国古代史', '3', '30', '09');
INSERT INTO `course` VALUES ('08306013', '中国近现代史', '3', '30', '09');
INSERT INTO `course` VALUES ('08306014', '西方哲学史', '4', '40', '18');
INSERT INTO `course` VALUES ('08306015', '逻辑学', '4', '40', '18');
INSERT INTO `course` VALUES ('08306016', '伦理学', '4', '40', '18');
INSERT INTO `course` VALUES ('08306017', '概率论', '3', '30', '11');
INSERT INTO `course` VALUES ('08306018', '数理统计学', '3', '30', '11');
INSERT INTO `course` VALUES ('08306019', '微积分', '4', '40', '11');
INSERT INTO `course` VALUES ('08306020', '力学', '4', '40', '12');

-- ----------------------------
-- Table structure for course_selection
-- ----------------------------
DROP TABLE IF EXISTS `course_selection`;
CREATE TABLE `course_selection`  (
  `student_id` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学号',
  `semester` char(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学期',
  `course_id` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '课号',
  `staff_id` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '工号',
  `score` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '成绩',
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  INDEX `fk_course_selection_course`(`course_id` ASC) USING BTREE,
  INDEX `fk_course_selection_teacher`(`staff_id` ASC) USING BTREE,
  CONSTRAINT `course_selection_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '选课表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course_selection
-- ----------------------------
INSERT INTO `course_selection` VALUES ('1101', '201201', '08305001', '0103', '69');
INSERT INTO `course_selection` VALUES ('1102', '201201', '08305001', '0103', '94');
INSERT INTO `course_selection` VALUES ('1102', '201202', '08305002', '0101', '82');
INSERT INTO `course_selection` VALUES ('1102', '201301', '08305004', '0101', '70');
INSERT INTO `course_selection` VALUES ('1103', '201202', '08305002', '0102', '75');
INSERT INTO `course_selection` VALUES ('1103', '201202', '08305003', '0102', '84');
INSERT INTO `course_selection` VALUES ('1103', '201301', '08305001', '0102', '84');
INSERT INTO `course_selection` VALUES ('1103', '201301', '08305004', '0101', '70');
INSERT INTO `course_selection` VALUES ('1104', '201302', '08302001', '0201', '70');
INSERT INTO `course_selection` VALUES ('1106', '201202', '08305002', '0103', '66');
INSERT INTO `course_selection` VALUES ('1107', '201202', '08305003', '0102', '79');
INSERT INTO `course_selection` VALUES ('1108', '202301', '08302002', '0202', '75');
INSERT INTO `course_selection` VALUES ('1109', '202301', '08302003', '0202', '80');
INSERT INTO `course_selection` VALUES ('1110', '202301', '08302004', '0203', '85');
INSERT INTO `course_selection` VALUES ('1103', '201201', '08305001', '0103', '69');
INSERT INTO `course_selection` VALUES ('1104', '201201', '08305001', '0103', '70');
INSERT INTO `course_selection` VALUES ('1105', '201201', '08305001', '0103', '71');
INSERT INTO `course_selection` VALUES ('1106', '201201', '08305001', '0103', '72');
INSERT INTO `course_selection` VALUES ('1107', '201201', '08305001', '0103', '74');
INSERT INTO `course_selection` VALUES ('1108', '201201', '08305001', '0103', '74');
INSERT INTO `course_selection` VALUES ('1109', '201201', '08305001', '0103', '74');
INSERT INTO `course_selection` VALUES ('1110', '201201', '08305001', '0103', '74');
INSERT INTO `course_selection` VALUES ('1103', '201302', '08302001', '0201', '60');
INSERT INTO `course_selection` VALUES ('1103', '202301', '08302002', '0202', '60');
INSERT INTO `course_selection` VALUES ('1103', '202301', '08302003', '0202', '60');
INSERT INTO `course_selection` VALUES ('1103', '202301', '08302004', '0203', '60');
INSERT INTO `course_selection` VALUES ('1103', '201202', '08305002', '0101', '60');
INSERT INTO `course_selection` VALUES ('1103', '201202', '08305002', '0103', '60');
INSERT INTO `course_selection` VALUES ('1104', '201201', '08305002', '0103', '40');
INSERT INTO `course_selection` VALUES ('1104', '201202', '08305002', '0103', '59');
INSERT INTO `course_selection` VALUES ('1105', '201201', '08305002', '0103', '59');
INSERT INTO `course_selection` VALUES ('1103', '201302', '08301001', '0210', '90');
INSERT INTO `course_selection` VALUES ('1101', '202401', '08306019', '0236', NULL);
INSERT INTO `course_selection` VALUES ('1101', '202401', '08306020', '0236', NULL);
INSERT INTO `course_selection` VALUES ('1101', '202301', '08302004', '0203', NULL);
INSERT INTO `course_selection` VALUES ('1101', '202401', '08306018', '0235', NULL);
INSERT INTO `course_selection` VALUES ('1101', '202401', '08306001', '0221', NULL);
INSERT INTO `course_selection` VALUES ('1101', '202401', '08306005', '0213', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08301001', '0210', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08301002', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08301003', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08301004', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302001', '0201', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302002', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302003', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302004', '0203', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302005', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302006', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302007', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302008', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302009', '0211', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302010', '0212', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302011', '0213', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302012', '0214', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302013', '0215', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302014', '0216', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302015', '0217', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302016', '0218', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302017', '0219', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302018', '0220', NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302019', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1113', '20231', '08302020', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08301001', '0210', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08301002', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08301003', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08301004', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302001', '0201', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302002', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302003', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302004', '0203', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302005', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302006', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302007', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302008', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302009', '0211', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302010', '0212', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302011', '0213', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302012', '0214', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302013', '0215', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302014', '0216', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302015', '0217', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302016', '0218', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302017', '0219', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302018', '0220', NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302019', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1114', '20231', '08302020', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08301001', '0210', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08301002', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08301003', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08301004', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302001', '0201', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302002', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302003', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302004', '0203', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302005', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302006', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302007', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302008', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302009', '0211', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302010', '0212', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302011', '0213', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302012', '0214', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302013', '0215', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302014', '0216', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302015', '0217', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302016', '0218', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302017', '0219', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302018', '0220', NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302019', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1115', '20231', '08302020', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08301001', '0210', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08301002', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08301003', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08301004', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302001', '0201', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302002', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302003', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302004', '0203', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302005', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302006', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302007', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302008', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302009', '0211', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302010', '0212', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302011', '0213', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302012', '0214', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302013', '0215', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302014', '0216', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302015', '0217', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302016', '0218', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302017', '0219', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302018', '0220', NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302019', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1116', '20231', '08302020', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08301001', '0210', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08301002', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08301003', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08301004', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302001', '0201', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302002', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302003', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302004', '0203', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302005', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302006', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302007', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302008', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302009', '0211', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302010', '0212', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302011', '0213', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302012', '0214', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302013', '0215', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302014', '0216', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302015', '0217', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302016', '0218', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302017', '0219', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302018', '0220', NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302019', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1117', '20231', '08302020', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08301001', '0210', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08301002', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08301003', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08301004', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302001', '0201', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302002', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302003', '0202', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302004', '0203', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302005', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302006', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302007', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302008', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302009', '0211', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302010', '0212', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302011', '0213', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302012', '0214', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302013', '0215', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302014', '0216', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302015', '0217', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302016', '0218', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302017', '0219', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302018', '0220', NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302019', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1118', '20231', '08302020', NULL, NULL);
INSERT INTO `course_selection` VALUES ('1119', '20231', '08301001', '0210', NULL);
INSERT INTO `course_selection` VALUES ('1101', '201202', '08305003', '0102', '90');
INSERT INTO `course_selection` VALUES ('1101', '202301', '08302002', '0202', '61');
INSERT INTO `course_selection` VALUES ('1101', '202301', '08302003', '0202', '80');
INSERT INTO `course_selection` VALUES ('1101', '201302', '08301001', '0210', '75');
INSERT INTO `course_selection` VALUES ('1101', '201302', '08302001', '0201', '60');

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department`  (
  `dept_id` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '院系号',
  `dept_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '名称',
  `address` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地址',
  `phone_code` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '联系电话',
  PRIMARY KEY (`dept_id`) USING BTREE,
  UNIQUE INDEX `unique_dept_id`(`dept_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '院系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES ('01', '计算机学院', '上大东校区三号楼', '65347567');
INSERT INTO `department` VALUES ('02', '通讯学院', '上大东校区二号楼', '65341234');
INSERT INTO `department` VALUES ('03', '材料学院', '上大东校区四号楼', '65347890');
INSERT INTO `department` VALUES ('04', '经济学院', '上大东校区五号楼', '65348888');
INSERT INTO `department` VALUES ('05', '外语学院', '上大东校区六号楼', '65349999');
INSERT INTO `department` VALUES ('06', '法学院', '上大东校区七号楼', '65341111');
INSERT INTO `department` VALUES ('07', '艺术学院', '上大东校区八号楼', '65342222');
INSERT INTO `department` VALUES ('08', '医学院', '上大东校区九号楼', '65343333');
INSERT INTO `department` VALUES ('09', '历史学院', '上大东校区十号楼', '65344444');
INSERT INTO `department` VALUES ('10', '化学学院', '上大东校区十一号楼', '65345555');
INSERT INTO `department` VALUES ('11', '数学学院', '上大东校区十二号楼', '65346666');
INSERT INTO `department` VALUES ('12', '物理学院', '上大东校区十三号楼', '65347777');
INSERT INTO `department` VALUES ('13', '生物学院', '上大东校区十四号楼', '65348888');
INSERT INTO `department` VALUES ('14', '地理学院', '上大东校区十五号楼', '65349999');
INSERT INTO `department` VALUES ('15', '政治学院', '上大东校区十六号楼', '65341111');
INSERT INTO `department` VALUES ('16', '心理学院', '上大东校区十七号楼', '65342222');
INSERT INTO `department` VALUES ('17', '社会学院', '上大东校区十八号楼', '65343333');
INSERT INTO `department` VALUES ('18', '哲学学院', '上大东校区十九号楼', '65344444');
INSERT INTO `department` VALUES ('19', '地球科学学院', '上大东校区二十号楼', '65345555');
INSERT INTO `department` VALUES ('20', '环境科学学院', '上大东校区二十一号楼', '65346666');
INSERT INTO `department` VALUES ('21', '大气科学学院', '上大东校区二十二号楼', '65347777');
INSERT INTO `department` VALUES ('22', '工程科学学院', '上大东校区二十三号楼', '65348888');
INSERT INTO `department` VALUES ('23', '生态学院', '上大东校区二十四号楼', '65349999');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `student_id` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '学号',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '姓名',
  `sex` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `date_of_birth` date NULL DEFAULT NULL,
  `native_place` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '籍贯',
  `mobile_phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号码',
  `dept_id` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '院系号',
  `Status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`student_id`) USING BTREE,
  UNIQUE INDEX `unique_student_id`(`student_id` ASC) USING BTREE,
  INDEX `idx1`(`dept_id` ASC, `name` DESC) USING BTREE,
  CONSTRAINT `student_dept_fk` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '学生表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('1101', '李明', '男', '1993-03-06', '上海', '13613005486', '02', NULL, '$2a$12$AUguFG5WbhWj9ae7Pst/5exCD9Nm/z6CjKT6CcE9jlxV4FUFR0Ynq');
INSERT INTO `student` VALUES ('1102', '刘晓明', '男', '1992-12-08', '安徽', '18913457890', '01', NULL, '$2a$12$0fSchPNp.7CrIJlx.cBoTOrjQfjdMeCAqmzEg.se26uwtf4oiCE3u');
INSERT INTO `student` VALUES ('1103', '张颖', '女', '1993-01-05', '江苏', '18826490423', '01', NULL, '$2a$12$2ypxOpGVXGHg7gv.cwI57eM8qv5CJrp2TbsD7cX0BswnrAXfiKlfm');
INSERT INTO `student` VALUES ('1104', '刘晶晶', '女', '1994-11-06', '上海', '13331934111', '01', NULL, '$2a$12$0F6.2viOdS8w2Qv717HFKuTgywdnBnvIoQwUifoj9Z2rFsSmjUYiy');
INSERT INTO `student` VALUES ('1105', '刘成刚', '男', '1991-06-07', '上海', '18015872567', '01', NULL, '$2a$12$2sozqrMOVRVjMtfML/9.eOCaMLMRo76301wOcwZaAr3NFLjvshxH.');
INSERT INTO `student` VALUES ('1106', '李二丽', '女', '1993-05-04', '江苏', '18107620945', '01', NULL, '$2a$12$taL7YbOe9mK9z/rWTuvidu9nlB7xwvsYxEVUpV9eng5P9TMu/Zu6W');
INSERT INTO `student` VALUES ('1107', '张晓峰', '男', '1992-08-16', '浙江', '13912341078', '01', NULL, '$2a$12$fkrn0uj0ou3pzSnVlatoGemAraPjdvcNH/uCdS1kTfzKquCjGB/r6');
INSERT INTO `student` VALUES ('1108', '张三', '男', '2001-01-01', '某地', '12345678901', '01', NULL, '$2a$12$NPwPujKaPLhErK5zc9UWoOGWO.XBbZATy8K9uOzHfP4ld.3hGWd9K');
INSERT INTO `student` VALUES ('1109', '李四', '男', '2002-02-02', '某地', '12345678902', '01', NULL, '$2a$12$fWLHxSQCgqL8KCnMAILSY.ID41y1AEmOdnLRHo8X5CfMf8nTqWynm');
INSERT INTO `student` VALUES ('1110', '王五', '男', '2000-03-03', '某地', '12345678903', '01', NULL, '$2a$12$PyCg1umvt1wSTIWYFhL/RueBsJE/963cLGwv.sAO2/4WQZew2Og.a');
INSERT INTO `student` VALUES ('1111', '邱逸轩', '男', '2001-01-01', '北京', '12345678909', '01', NULL, '$2a$12$AWxd7rabFWUzd1G0KnxzI.aJUmHr5lkZ2EkRIUU8d.b8MxNajKlQi');
INSERT INTO `student` VALUES ('1112', '马英九', '男', '1998-12-13', '北京', '12345678909', '02', NULL, '$2a$12$e/w3iWdEtb5gG.g.s6.c1eFrAbtNW7WOwfVe55.AW6ItTicNXcmqq');
INSERT INTO `student` VALUES ('1113', '张三', '男', '2003-01-01', '北京', '13812345678', '01', 'A', '$2a$12$HHx.z31KAlPfYM4kla6cP.S6QpSV.nsqhWwN4bG5Sgew1Z0XrJAH.');
INSERT INTO `student` VALUES ('1114', '李四', '男', '2003-02-02', '上海', '13912345678', '02', 'A', '$2a$12$4nhHTnb1CURopaug6XuxfOS8cN33QZSdRLtOY2bYNcQiiW9dg3JS.');
INSERT INTO `student` VALUES ('1115', '王五', '男', '2003-03-03', '广州', '13712345678', '03', 'A', '$2a$12$YQkDWAonfYX3JDv4QNddk.LT1u/.68qLL2FZ/A0zmPpJcxGYp63d6');
INSERT INTO `student` VALUES ('1116', '赵六', '男', '2003-04-04', '深圳', '13612345678', '04', 'A', '$2a$12$aRfKJOUaTLXXQUNXdJq2qO7k4TWJwh9jU5eg77xbMmViN21mTNWUe');
INSERT INTO `student` VALUES ('1117', '钱七', '男', '2003-05-05', '成都', '13512345678', '05', 'A', '$2a$12$5NU8QHh.a6fouyv8oCXcfeLUljEuw8HKwCj9XMCFEjer4NOlLcxii');
INSERT INTO `student` VALUES ('1118', '孙八', '女', '2003-06-06', '重庆', '13412345678', '06', 'A', '$2a$12$FbzaEfxsZeV/rZqKVB7siOsYkD2TvtX7V8t0kqbj//.ePfScPe8.a');
INSERT INTO `student` VALUES ('1119', '周九', '女', '2003-07-07', '武汉', '13312345678', '07', 'A', '$2a$12$fltiVtTseV..EcZRisMjm.K.VyqLoLAq21UxZT75JJ9vtY.vU/ZJa');
INSERT INTO `student` VALUES ('1120', '吴十', '女', '2003-08-08', '西安', '13212345678', '08', 'A', '$2a$12$tPDraOZMjyYQYho6XoSQ3etMhcziptbJtH6XfW5CX/JiMGbVCtcdm');
INSERT INTO `student` VALUES ('1121', '郑十一', '女', '2003-09-09', '南京', '13112345678', '09', 'A', '$2a$12$dKlIqOgDGzA3iq7OzSaqOOpq6vdAkmM3lFHkJ79U3G5towXj.rTjO');
INSERT INTO `student` VALUES ('1122', '王十二', '女', '2003-10-10', '杭州', '13012345678', '10', 'A', '$2a$12$yr8gOYSXX3oOidkmZV47Ee1aSFUBEARjRA0lIaiCDBz6p9nFETpQ2');
INSERT INTO `student` VALUES ('1123', '赵十三', '女', '2003-11-11', '苏州', '13912345677', '01', 'A', '$2a$12$sjkVkErRgF4.9km20S64euttnH0/JJ/i/Yd3esD0oHuVQ4gVEcN5i');
INSERT INTO `student` VALUES ('1124', '钱十四', '女', '2003-12-12', '天津', '13912345676', '02', 'A', '$2a$12$0CPM7t7FYNgnCiO/6tCuSeSKTryGgJEs3oh3/Qf7JcD9JaCAWYw5e');
INSERT INTO `student` VALUES ('1125', '孙十五', '女', '2004-01-01', '重庆', '13912345675', '03', 'A', '$2a$12$EWQmUIFLBucErGZjYnFS/ejfdmYtHXFPNk72wnK6/LIP0Dxq82RgK');
INSERT INTO `student` VALUES ('1126', '周十六', '女', '2004-02-02', '成都', '13912345674', '04', 'A', '$2a$12$hpmsPzKw2d/wK7EOVAv85.PKS/lROPUAdZE45mfbcN.ZT0Q3AsiWu');
INSERT INTO `student` VALUES ('1127', '吴十七', '女', '2004-03-03', '广州', '13912345673', '05', 'A', '$2a$12$rUCEAd8KBfRbJsmkKRTXbemjJWELDt6oZ10hgMKTL/Ckc8Ni7WQHq');
INSERT INTO `student` VALUES ('1128', '郑十八', '女', '2004-04-04', '上海', '13912345672', '06', 'A', '$2a$12$jmm5qICfXUDz7LGqf9XmjOcGy.dg4Mrl0Uw0chANFeCtsWV0dQxam');
INSERT INTO `student` VALUES ('1129', '王十九', '女', '2004-05-05', '北京', '13912345671', '07', 'A', '$2a$12$SMA/wh9EkEmjK9ke6nNkeeywIsLzFebjCcmzIYYfmIgh8ZG91a8La');
INSERT INTO `student` VALUES ('1130', '李二十', '女', '2004-06-06', '杭州', '13912345670', '08', 'A', '$2a$12$rte8aLvQ6t6c8JEomrg9Qemc5B0k0jxuOASTkCN0dGi8ce1R3XBiO');
INSERT INTO `student` VALUES ('1131', '小明', '男', '2004-07-07', '苏州', '13912345679', '09', 'A', '$2a$12$OGx.6zYz4CULWjG03ZcxLuNH6jgrLQTn/fbaLxmg3giAwFdt7307S');
INSERT INTO `student` VALUES ('1132', '小红', '女', '2004-08-08', '天津', '13912345678', '10', 'A', '$2a$12$5LsYG3VPLSYnZ8uTjXtSAOXaIAVUzuruQmLWeQ6lJAe6/xM8UGBom');

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `staff_id` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '工号',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '姓名',
  `sex` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `date_of_birth` date NULL DEFAULT NULL,
  `professional_ranks` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '职称',
  `salary` float(6, 2) NULL DEFAULT NULL COMMENT '基本工资',
  `dept_id` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '院系号',
  PRIMARY KEY (`staff_id`) USING BTREE,
  INDEX `teacher_dept_fk`(`dept_id` ASC) USING BTREE,
  CONSTRAINT `teacher_dept_fk` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `chk_salary_teacher` CHECK ((`sex` <> _utf8mb4'男') or (`salary` > 6500)),
  CONSTRAINT `chk_sex` CHECK (`sex` in (_utf8mb4'男',_utf8mb4'女'))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '教师表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES ('0101', '陈迪茂', '男', '1983-03-06', '副教授', 7567.00, '01');
INSERT INTO `teacher` VALUES ('0102', '马小红', '女', '1992-12-08', '讲师', 5845.00, '01');
INSERT INTO `teacher` VALUES ('0103', '吴宝钢', '男', '1990-11-06', '讲师', 6501.00, '01');
INSERT INTO `teacher` VALUES ('0201', '张心颖', '女', '1970-01-05', '教授', 9200.00, '02');
INSERT INTO `teacher` VALUES ('0202', '邱逸轩', '男', '1970-01-01', '教授', 9999.00, '01');
INSERT INTO `teacher` VALUES ('0203', '林哲', '男', '1975-01-01', '教授', 9999.00, '01');
INSERT INTO `teacher` VALUES ('0204', '蛋蛋', '男', '1975-01-01', '教授', 6600.00, '01');
INSERT INTO `teacher` VALUES ('0206', '轩轩', '男', '1975-01-01', '教授', 6600.00, '01');
INSERT INTO `teacher` VALUES ('0207', '哲哲', '女', '1998-01-01', '教授', 3500.00, '01');
INSERT INTO `teacher` VALUES ('0208', '轩轩子', '女', '1998-01-01', '副教授', 6600.00, '01');
INSERT INTO `teacher` VALUES ('0209', '小轩轩', '男', '1999-01-01', '副教授', 7000.00, '01');
INSERT INTO `teacher` VALUES ('0210', '邱小轩', '男', '1975-01-01', '教授', 6600.00, '03');
INSERT INTO `teacher` VALUES ('0211', '李小龙', '男', '1985-05-15', '副教授', 7200.00, '03');
INSERT INTO `teacher` VALUES ('0212', '王小花', '女', '1990-08-20', '讲师', 5800.00, '03');
INSERT INTO `teacher` VALUES ('0213', '张大山', '男', '1978-10-10', '教授', 9000.00, '04');
INSERT INTO `teacher` VALUES ('0214', '李小云', '女', '1988-03-25', '副教授', 7000.00, '05');
INSERT INTO `teacher` VALUES ('0215', '赵小明', '男', '1992-06-30', '讲师', 6800.00, '06');
INSERT INTO `teacher` VALUES ('0216', '孙小红', '女', '1995-09-05', '助教', 5000.00, '07');
INSERT INTO `teacher` VALUES ('0217', '周小刚', '男', '1980-12-12', '教授', 9200.00, '08');
INSERT INTO `teacher` VALUES ('0218', '郑小萍', '女', '1985-01-20', '副教授', 7500.00, '09');
INSERT INTO `teacher` VALUES ('0219', '唐小磊', '男', '1976-04-28', '教授', 9800.00, '10');
INSERT INTO `teacher` VALUES ('0220', '梁小燕', '女', '1982-07-15', '讲师', 6000.00, '11');
INSERT INTO `teacher` VALUES ('0221', '王小明', '男', '1975-05-15', '教授', 8800.00, '09');
INSERT INTO `teacher` VALUES ('0222', '刘小红', '女', '1988-09-25', '副教授', 7200.00, '09');
INSERT INTO `teacher` VALUES ('0223', '张小刚', '男', '1990-06-20', '讲师', 6800.00, '09');
INSERT INTO `teacher` VALUES ('0224', '赵小雪', '女', '1995-03-10', '助教', 5000.00, '10');
INSERT INTO `teacher` VALUES ('0225', '钱小明', '男', '1978-07-28', '教授', 9500.00, '10');
INSERT INTO `teacher` VALUES ('0226', '孙小雨', '女', '1985-11-15', '副教授', 7800.00, '10');
INSERT INTO `teacher` VALUES ('0227', '李小峰', '男', '1992-04-20', '讲师', 6900.00, '10');
INSERT INTO `teacher` VALUES ('0228', '周小雪', '女', '1998-02-05', '助教', 5200.00, '15');
INSERT INTO `teacher` VALUES ('0229', '吴小龙', '男', '1982-09-10', '教授', 9300.00, '15');
INSERT INTO `teacher` VALUES ('0230', '郑小雨', '女', '1987-06-18', '副教授', 7600.00, '15');
INSERT INTO `teacher` VALUES ('0231', '王小风', '男', '1976-08-25', '教授', 9600.00, '17');
INSERT INTO `teacher` VALUES ('0232', '冯小雪', '女', '1989-12-30', '副教授', 7900.00, '17');
INSERT INTO `teacher` VALUES ('0233', '陈小刚', '男', '1993-02-15', '讲师', 6800.00, '17');
INSERT INTO `teacher` VALUES ('0234', '黄小红', '女', '1996-07-05', '助教', 5300.00, '18');
INSERT INTO `teacher` VALUES ('0235', '林小明', '男', '1983-10-20', '教授', 9400.00, '18');
INSERT INTO `teacher` VALUES ('0236', '张小玉', '女', '1988-04-18', '副教授', 7700.00, '18');
INSERT INTO `teacher` VALUES ('0237', '杨小雪', '女', '1991-11-10', '讲师', 6400.00, '18');
INSERT INTO `teacher` VALUES ('0238', '徐小刚', '男', '1979-06-28', '教授', 9700.00, '19');
INSERT INTO `teacher` VALUES ('0239', '朱小明', '女', '1984-01-15', '副教授', 8000.00, '19');
INSERT INTO `teacher` VALUES ('0240', '秦小雨', '女', '1989-09-20', '讲师', 6500.00, '19');
INSERT INTO `teacher` VALUES ('0241', '谢小刚', '男', '1977-03-10', '教授', 9800.00, '20');
INSERT INTO `teacher` VALUES ('0242', '罗小红', '女', '1982-08-05', '副教授', 8200.00, '20');
INSERT INTO `teacher` VALUES ('0243', '程小明', '男', '1989-01-18', '讲师', 6600.00, '20');
INSERT INTO `teacher` VALUES ('0244', '曹小雪', '女', '1994-05-25', '助教', 5500.00, '21');
INSERT INTO `teacher` VALUES ('0245', '康小雨', '女', '1997-11-30', '教授', 9900.00, '21');
INSERT INTO `teacher` VALUES ('0246', '金小明', '男', '1980-07-15', '副教授', 8300.00, '21');
INSERT INTO `teacher` VALUES ('0247', '魏小刚', '男', '1984-09-18', '讲师', 6700.00, '21');
INSERT INTO `teacher` VALUES ('0248', '丁小红', '女', '1990-02-10', '教授', 9000.00, '22');
INSERT INTO `teacher` VALUES ('0249', '董小雪', '女', '1993-06-05', '副教授', 8500.00, '22');
INSERT INTO `teacher` VALUES ('0250', '卢小明', '男', '1975-08-20', '讲师', 6800.00, '22');
INSERT INTO `teacher` VALUES ('0251', '孔小雨', '女', '1988-04-28', '助教', 5600.00, '22');
INSERT INTO `teacher` VALUES ('0252', '陶小刚', '男', '1992-12-15', '教授', 9200.00, '23');
INSERT INTO `teacher` VALUES ('0253', '章小红', '女', '1995-08-05', '副教授', 8700.00, '23');
INSERT INTO `teacher` VALUES ('0254', '程小明', '男', '1981-02-18', '讲师', 6900.00, '23');
INSERT INTO `teacher` VALUES ('0255', '邓小雪', '女', '1986-11-30', '助教', 5700.00, '23');

-- ----------------------------
-- View structure for scoreless
-- ----------------------------
DROP VIEW IF EXISTS `scoreless`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `scoreless` AS select `s`.`student_id` AS `student_id`,`s`.`name` AS `name`,`s`.`sex` AS `sex`,`s`.`mobile_phone` AS `mobile_phone`,`c`.`course_name` AS `course_name`,`cs`.`score` AS `score` from ((`student` `s` join `course_selection` `cs` on((`s`.`student_id` = `cs`.`student_id`))) join `course` `c` on((`cs`.`course_id` = `c`.`course_id`))) where ((`cs`.`score` < 60) and (`c`.`course_id` = `cs`.`course_id`) and (`s`.`dept_id` = '01'));

-- ----------------------------
-- Procedure structure for insertTestData
-- ----------------------------
DROP PROCEDURE IF EXISTS `insertTestData`;
delimiter ;;
CREATE PROCEDURE `insertTestData`()
BEGIN
  DECLARE current_count INT;
  SELECT MAX(id) INTO current_count FROM test_data;
  IF current_count IS NULL THEN
    SET current_count = 0;
  END IF;
  WHILE current_count < 10000000 DO
    INSERT INTO test_data (data_field, indexed_field) VALUES (CONCAT('Data ', current_count), current_count);
    SET current_count = current_count + 1;
  END WHILE;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table course_selection
-- ----------------------------
DROP TRIGGER IF EXISTS `check_valid_score_before_insert`;
delimiter ;;
CREATE TRIGGER `check_valid_score_before_insert` BEFORE INSERT ON `course_selection` FOR EACH ROW BEGIN
    IF NEW.score IS NOT NULL AND (NEW.score < 0 OR NEW.score > 100) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '成绩必须在0到100分之间';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table course_selection
-- ----------------------------
DROP TRIGGER IF EXISTS `check_valid_score_before_update`;
delimiter ;;
CREATE TRIGGER `check_valid_score_before_update` BEFORE UPDATE ON `course_selection` FOR EACH ROW BEGIN
    IF NEW.score IS NOT NULL AND (NEW.score < 0 OR NEW.score > 100) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '成绩必须在0到100分之间';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table student
-- ----------------------------
DROP TRIGGER IF EXISTS `before_student_insert_or_update`;
delimiter ;;
CREATE TRIGGER `before_student_insert_or_update` BEFORE INSERT ON `student` FOR EACH ROW BEGIN
  IF NEW.sex NOT IN ('男', '女') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = '性别只能是男或女';
  END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table student
-- ----------------------------
DROP TRIGGER IF EXISTS `before_student_update`;
delimiter ;;
CREATE TRIGGER `before_student_update` BEFORE UPDATE ON `student` FOR EACH ROW BEGIN
  IF NEW.sex NOT IN ('男', '女') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = '性别只能是男或女';
  END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table teacher
-- ----------------------------
DROP TRIGGER IF EXISTS `before_teacher_insert`;
delimiter ;;
CREATE TRIGGER `before_teacher_insert` BEFORE INSERT ON `teacher` FOR EACH ROW BEGIN
  IF NEW.sex NOT IN ('男', '女') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = '性别只能是男或女';
  END IF;
  IF NEW.sex = '男' AND NEW.salary <= 6500 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = '男性教师工资必须超过6500元';
  END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
