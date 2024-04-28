from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import logging
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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(courses=courses)
