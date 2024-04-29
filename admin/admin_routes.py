from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import mysql.connector
from config.db_config import get_db_connection

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/courses')
def manage_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_courses.html', courses=courses)


@admin_bp.route('/students')
def manage_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_students.html', students=students)


@admin_bp.route('/teachers')
def manage_teachers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teacher")
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_teachers.html', teachers=teachers)

@admin_bp.route('/departments')
def manage_departments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM department")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_departments.html', departments=departments)

@admin_bp.route('/classes')
def manage_classes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class")
    classes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_classes.html', classes=classes)


@admin_bp.route('/api/add_course', methods=['POST'])
def add_course():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # 首先验证部门ID是否存在
    cursor.execute("SELECT 1 FROM department WHERE dept_id = %s", (data['dept_id'],))
    if cursor.fetchone() is None:
        return jsonify({'success': False, 'message': '指定的部门ID不存在'}), 400

    try:
        sql = "INSERT INTO course (course_id, course_name, credit, credit_hours, dept_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (data['course_id'], data['course_name'], data['credit'], data['credit_hours'], data['dept_id']))
        conn.commit()
        return jsonify({'success': True, 'message': '课程添加成功'})
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': '数据库错误: ' + str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/api/delete_course/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Course deleted successfully'})


# Add this endpoint definition under the admin_bp blueprint
@admin_bp.route('/course_list')
def course_list():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql_query = """
                SELECT * FROM course
                WHERE course_id LIKE %s OR course_name LIKE %s
            """
    cursor.execute(sql_query, ('%' + query + '%', '%' + query + '%'))
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(courses=courses)

@admin_bp.route('/api/add_student', methods=['POST'])
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # 首先验证部门ID是否存在
    cursor.execute("SELECT 1 FROM department WHERE dept_id = %s", (data['dept_id'],))
    if cursor.fetchone() is None:
        return jsonify({'success': False, 'message': '指定的部门ID不存在'}), 400

    try:
        sql = "INSERT INTO student (student_id, name, sex, date_of_birth, native_place, mobile_phone, dept_id, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            data['student_id'],
            data['name'],
            data['sex'],
            data['date_of_birth'],
            data['native_place'],
            data['mobile_phone'],
            data['dept_id'],
            data['Status']
        ))
        conn.commit()
        return jsonify({'success': True, 'message': '学生添加成功'})
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': '数据库错误: ' + str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/api/delete_student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # 首先检查学生是否已经选课
    cursor.execute("SELECT COUNT(*) FROM course_selection WHERE student_id = %s", (student_id,))
    course_count = cursor.fetchone()[0]
    if course_count > 0:
        # 如果已选课程，则不允许删除
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': '无法删除，该学生已选课！'}), 400

    try:
        # 如果未选课程，则尝试删除学生
        cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '学生删除成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': '删除学生时发生错误: {}'.format(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Add this endpoint definition under the admin_bp blueprint
@admin_bp.route('/student_list')
def student_list():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql_query = """
            SELECT * FROM student
            WHERE student_id LIKE %s OR name LIKE %s OR native_place like %s OR sex like %s OR dept_id like %s
        """
    cursor.execute(sql_query, ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students=students)


@admin_bp.route('/api/add_teacher', methods=['POST'])
def add_teacher():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # 首先验证部门ID是否存在
    cursor.execute("SELECT 1 FROM department WHERE dept_id = %s", (data['dept_id'],))
    if cursor.fetchone() is None:
        return jsonify({'success': False, 'message': '指定的部门ID不存在'}), 400

    try:
        sql = "INSERT INTO teacher (staff_id, name, sex, date_of_birth, professional_ranks, salary, dept_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            data['staff_id'],
            data['name'],
            data['sex'],
            data['date_of_birth'],
            data['professional_ranks'],
            data['salary'],
            data['dept_id']
        ))
        conn.commit()
        return jsonify({'success': True, 'message': '教师添加成功'})
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': '数据库错误: ' + str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/api/delete_teacher/<staff_id>', methods=['DELETE'])
def delete_teacher(staff_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # 首先检查教师是否已经选课
    cursor.execute("SELECT COUNT(*) FROM class WHERE staff_id = %s", (staff_id,))
    course_count = cursor.fetchone()[0]
    if course_count > 0:
        # 如果已选课程，则不允许删除
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': '无法删除，该教师已开课！'}), 400

    try:
        # 如果未选课程，则尝试删除教师
        cursor.execute("DELETE FROM teacher WHERE staff_id = %s", (staff_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '教师删除成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': '删除教师时发生错误: {}'.format(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Add this endpoint definition under the admin_bp blueprint
@admin_bp.route('/teacher_list')
def teacher_list():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql_query = """
        SELECT * FROM teacher
        WHERE staff_id LIKE %s OR name LIKE %s OR professional_ranks like %s OR sex like %s OR dept_id like %s
        """
    cursor.execute(sql_query, ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(teachers=teachers)

@admin_bp.route('/api/add_department', methods=['POST'])
def add_department():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO department (dept_id, dept_name, address, phone_code) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (
            data['dept_id'],
            data['dept_name'],
            data['address'],
            data['phone_code']
        ))
        conn.commit()
        return jsonify({'success': True, 'message': '院系添加成功'})
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': '数据库错误: ' + str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/api/delete_department/<dept_id>', methods=['DELETE'])
def delete_department(dept_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # 首先检查院系是否已经选课
    cursor.execute("SELECT COUNT(*) FROM teacher WHERE dept_id = %s", (dept_id,))
    course_count = cursor.fetchone()[0]
    if course_count > 0:
        # 如果已选课程，则不允许删除
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': '无法删除，该院系已开课！'}), 400

    try:
        # 如果未选课程，则尝试删除院系
        cursor.execute("DELETE FROM department WHERE dept_id = %s", (dept_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '院系删除成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': '删除院系时发生错误: {}'.format(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Add this endpoint definition under the admin_bp blueprint
@admin_bp.route('/department_list')
def department_list():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql_query = """
        SELECT * FROM department
        WHERE dept_id LIKE %s OR dept_name LIKE %s OR address like %s
        """
    cursor.execute(sql_query, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(departments=departments)








