from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, app
import logging
from config.db_config import get_db_connection

teacher_bp = Blueprint('teacher', __name__, template_folder='templates')


# 教师路由实现 ...

@teacher_bp.route('/teacher_management', methods=['GET', 'POST'])
def teacher_management():
    print("Received form data:", request.form)
    course_id = request.form.get('course_id')
    staff_id = request.form.get('staff_id')
    semester = request.form.get('semester')
    grade = request.form.get('grade')
    print(course_id)
    print(staff_id)
    print(semester)
    print(grade)
    # 使用这些参数来从数据库获取需要的数据
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.student_id, s.name, cs.score, course_id, semester
            FROM course_selection cs
            JOIN student s ON cs.student_id = s.student_id
            WHERE cs.course_id = %s AND cs.staff_id = %s AND cs.semester = %s
        """, (course_id, staff_id, semester))
        students = cursor.fetchall()
        print(students)
        return render_template('teacher_management.html', students=students, course_id=course_id, staff_id=staff_id, semester=semester)
    except Exception as err:
        print("An error occurred:", err)
        return str(err)  # 或其他错误处理方式
    finally:
        cursor.close()
        conn.close()


@teacher_bp.route('/update_grade', methods=['POST'])
def update_grade():
    data = request.json
    print("Received data:", data)
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    semester = data.get('semester')
    new_grade = data.get('new_grade')

    # 假设更新数据库代码如下
    # 确保 SQL 查询使用了正确的字段
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE course_selection
            SET score = %s
            WHERE student_id = %s AND course_id = %s AND semester = %s
        """, (new_grade, student_id, course_id, semester))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        print("Error updating grade:", e)
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({'success': True})

@teacher_bp.route('/grade_distribution', methods=['GET'])
def grade_distribution():
    course_id = request.args.get('course_id')
    semester = request.args.get('semester')
    staff_id = request.args.get('staff_id')
    print(semester)
    print(course_id)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 获取课程名称
        cursor.execute("SELECT course_name FROM course WHERE course_id = %s", (course_id,))
        course_name = cursor.fetchone()['course_name']

        # 获取成绩分布
        cursor.execute("""
            SELECT score_ranges.score_range, COALESCE(scores.count, 0) AS count
FROM (
    SELECT '0-59' AS score_range UNION ALL
    SELECT '60-69' UNION ALL
    SELECT '70-79' UNION ALL
    SELECT '80-89' UNION ALL
    SELECT '90-100'
) AS score_ranges
LEFT JOIN (
    SELECT
        CASE
            WHEN score >= 90 THEN '90-100'
            WHEN score >= 80 THEN '80-89'
            WHEN score >= 70 THEN '70-79'
            WHEN score >= 60 THEN '60-69'
            ELSE '0-59'
        END AS score_range,
        COUNT(*) AS count
    FROM course_selection
    WHERE course_id = %s AND semester = %s AND staff_id = %s
    GROUP BY score_range
) AS scores ON score_ranges.score_range = scores.score_range
ORDER BY FIELD(score_ranges.score_range, '90-100', '80-89', '70-79', '60-69', '0-59');

        """, (course_id, semester, staff_id,))
        distribution = cursor.fetchall()
        print(distribution)
        cursor.execute("""
            SELECT COUNT(*) AS total_students
            FROM course_selection
            WHERE course_id = %s AND semester = %s AND staff_id = %s
        """, (course_id, semester, staff_id))
        total_students = cursor.fetchone()
        print(distribution)
        print(total_students)
        return jsonify(course_name=course_name, distribution=distribution, total_students=total_students)
    except Exception as err:
        print("An error occurred:", err)
        return jsonify(error=str(err))
    finally:
        cursor.close()
        conn.close()
