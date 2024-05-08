from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, app
import logging
from config.db_config import get_db_connection

student_bp = Blueprint('student', __name__, template_folder='templates')


# 在学生模块的路由中定义获取课程信息的接口
@student_bp.route('/api/courses', methods=['GET'])
def get_courses():
    """
    获取指定学期的课程信息，支持通过查询参数进行课程名称、课程ID或教师姓名的模糊搜索。

    参数:
    - semester: 指定的学期
    - query: 用于课程名称、课程ID或教师姓名的模糊搜索的关键字

    返回值:
    - 一个包含课程信息的JSON对象，如果发生错误则返回包含错误信息的JSON对象。
    """
    # 从请求中获取学期和查询参数
    semester = request.args.get('semester')
    query = request.args.get('query', '')

    # 连接到数据库
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 构造SQL查询语句，以获取指定学期并匹配课程名称、课程ID或教师姓名的课程信息
        sql_query = """
        SELECT c.course_id, c.course_name, c.credit, d.dept_name, t.name as teacher_name
        FROM course c
        JOIN class cl ON c.course_id = cl.course_id
        JOIN teacher t ON cl.staff_id = t.staff_id
        JOIN department d ON c.dept_id = d.dept_id
        WHERE cl.semester = %s AND
              (c.course_name LIKE %s OR c.course_id LIKE %s OR t.name LIKE %s)
        """
        cursor.execute(sql_query, (semester, f'%{query}%', f'%{query}%', f'%{query}%'))
        # 执行查询并获取所有结果
        courses = cursor.fetchall()
        return jsonify(courses)
    except mysql.connector.Error as err:
        # 处理数据库错误，返回错误信息
        return jsonify({'error': str(err)}), 500
    finally:
        # 确保在查询结束后关闭数据库连接
        cursor.close()
        conn.close()


@student_bp.route('/api/selected_courses', methods=['GET'])
def get_selected_courses():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    semester = request.args.get('semester')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql_query = """
        SELECT c.course_id, c.course_name, cl.class_time, t.name as teacher_name, t.staff_id, c.credit
        FROM course_selection cs
        JOIN course c ON cs.course_id = c.course_id
        JOIN class cl ON cl.course_id = c.course_id AND cl.semester = cs.semester
        JOIN teacher t ON cl.staff_id = t.staff_id
        WHERE cs.student_id = %s AND cs.semester = %s
        """
        cursor.execute(sql_query, (user_id, semester))
        selected_courses = cursor.fetchall()
        return jsonify(selected_courses)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@student_bp.route('/list_courses', methods=['GET'])
def list_courses():
    """根据选定的学期显示课程列表。"""
    semester = request.args.get('semester')
    if not semester:
        return "Semester parameter is required", 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.credit, d.dept_name, t.name as teacher_name
            FROM class
            JOIN course c ON class.course_id = c.course_id
            JOIN department d ON c.dept_id = d.dept_id
            JOIN teacher t ON class.staff_id = t.staff_id
            WHERE class.semester = %s
        """, (semester,))
        courses = cursor.fetchall()
        return render_template('list_courses.html', courses=courses, semester=semester)
    except mysql.connector.Error as err:
        logging.error(f"查询课程信息错误: {err}")
        return "Error fetching courses from database", 500
    finally:
        conn.close()


@student_bp.route('/enroll_course', methods=['POST'])
def enroll_course():
    data = request.get_json()
    course_id = data['course_id']
    semester = data['semester']
    student_id = session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 检查该学生是否已经选择了这门课程
        cursor.execute("""
            SELECT * FROM course_selection 
            WHERE student_id = %s AND course_id = %s AND semester = %s
        """, (student_id, course_id, semester))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': '您已经选过这门课程。'}), 400

        # 从class表中获取对应课程的staff_id
        cursor.execute("""
            SELECT staff_id FROM class 
            WHERE course_id = %s AND semester = %s
        """, (course_id, semester))
        class_info = cursor.fetchone()
        if not class_info:
            return jsonify({'success': False, 'message': '未找到相关课程信息。'}), 404

        staff_id = class_info['staff_id']

        # 插入新的选课记录
        cursor.execute("""
            INSERT INTO course_selection (student_id, course_id, semester, staff_id) 
            VALUES (%s, %s, %s, %s)
        """, (student_id, course_id, semester, staff_id))
        conn.commit()
        return jsonify({'success': True}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        logging.error(f"数据库错误: {err}")
        return jsonify({'success': False, 'message': str(err)}), 500

    finally:
        cursor.close()
        conn.close()


@student_bp.route('/drop_course', methods=['POST'])
def drop_course():
    data = request.get_json()
    course_id = data['course_id']
    semester = data['semester']
    student_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM course_selection WHERE student_id = %s AND course_id = %s AND semester = %s',
                       (student_id, course_id, semester))
        conn.commit()
        return jsonify({'success': True}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': str(err)}), 400
    finally:
        cursor.close()
        conn.close()


# 查询已修课程
@student_bp.route('/api/completed_courses', methods=['GET'])
def get_completed_courses():
    # 获取请求中的参数
    student_id = session.get('user_id')

    # 查询数据库获取已修课程数据
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT
                course.course_id,
                course.course_name, 
                course_selection.semester, 
                teacher.name AS teacher_name, 
                course.credit, 
                course_selection.score 
            FROM 
                course_selection 
            JOIN 
                teacher ON course_selection.staff_id = teacher.staff_id 
            JOIN 
                course ON course_selection.course_id = course.course_id 
            WHERE 
                course_selection.student_id = %s AND course_selection.score IS NOT NULL
        ''', (student_id,))
        courses = cursor.fetchall()  # 获取所有符合条件的课程记录

        # 打印返回的课程数据到控制台
        for course in courses:
            print(course)
        return jsonify({'success': True, 'courses': courses}), 200
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': str(err)}), 400
    finally:
        cursor.close()
        conn.close()


@student_bp.route('/api/transcript', methods=['POST'])
def transcript():
    # 从 POST 请求的 JSON 载荷中获取数据
    data = request.get_json()
    student_id = session.get('user_id')
    semester = data.get('semester')
    print(f"学生ID: {student_id}, 学期: {semester}")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 获取学生信息
        cursor.execute("SELECT name FROM student WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()  # 获取学生信息
        print(f"学生信息: {student}")  # 输出学生信息
        if not student:
            return jsonify({"success": False, "message": "学生信息不存在"}), 404

        # 查询课程和计算绩点
        cursor.execute("""
            SELECT cs.course_id, c.course_name as course_name, cs.staff_id, c.credit, cs.score,
            CASE
                WHEN cs.score >= 90 THEN '4.0'
                WHEN cs.score >= 85 THEN '3.7'
                WHEN cs.score >= 80 THEN '3.3'
                WHEN cs.score >= 77 THEN '3.0'
                WHEN cs.score >= 73 THEN '2.7'
                WHEN cs.score >= 70 THEN '2.3'
                WHEN cs.score >= 67 THEN '2.0'
                WHEN cs.score >= 63 THEN '1.5'
                WHEN cs.score >= 60 THEN '1.0'
                ELSE 0
            END AS grade_point
            FROM course_selection cs
            JOIN course c ON cs.course_id = c.course_id
            WHERE cs.student_id = %s AND cs.semester = %s
            ORDER BY cs.semester
        """, (student_id, semester))
        courses = cursor.fetchall()
        print(f"课程详情: {courses}")  # 输出课程详情

        # 计算平均绩点
        total_points = sum(float(course['grade_point']) * float(course['credit']) for course in courses)
        total_credits = sum(float(course['credit']) for course in courses)
        average_grade_point = total_points / total_credits if total_credits else 0

        # 返回 JSON 数据
        return jsonify({
            "success": True,
            "student": student,
            "courses": courses,
            "average_grade_point": average_grade_point
        })
    except Exception as err:
        print(f"获取成绩数据出错: {err}")
        return jsonify({"success": False, "message": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
