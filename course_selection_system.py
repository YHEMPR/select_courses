from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import mysql.connector
import bcrypt
import logging

app = Flask(__name__)
app.secret_key = 'yhempr666'
logging.basicConfig(level=logging.DEBUG)

# 数据库连接参数
conn_params = {
    'database': 'school',
    'user': 'root',
    'password': '5201314Eminem',
    'host': 'localhost',
    'port': '3306',
    'auth_plugin': 'mysql_native_password'
}


def get_db_connection():
    """创建并返回数据库连接。"""
    return mysql.connector.connect(**conn_params)


def hash_password(password):
    """返回密码的bcrypt哈希值。"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(hashed_password, user_password):
    """校验提供的密码与存储的哈希值是否匹配。"""
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))


# 定义过滤器函数
def format_semester(semester):
    year = semester[:4]
    term_code = semester[4:]
    terms = {"01": "秋季学期", "02": "冬季学期", "03": "春季学期"}
    return f"{year} {terms.get(term_code, '未知学期')}"


# 注册过滤器到 Jinja2
app.jinja_env.filters['format_semester'] = format_semester


@app.route('/')
def index():
    """重定向到登录页面。"""
    return redirect(url_for('login'))


from flask import redirect, url_for


@app.route('/login', methods=['POST'])
def login():
    """处理登录请求。"""
    # 尝试获取JSON数据
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '无效的请求'}), 400

    # 从请求中获取学生ID和密码
    student_id = data.get('student_id')
    password = data.get('password')

    # 获取数据库连接和创建游标
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 查询学生信息
        cursor.execute('SELECT * FROM student WHERE student_id = %s', (student_id,))
        student = cursor.fetchone()

        # 检查学生是否存在并验证密码
        if student and check_password(student['password'], password):
            # 设置session信息
            session['user_id'] = student['student_id']
            session['role'] = 'student'
            logging.debug("登录成功，正在重定向到课程页面")
            # 登录成功，返回成功状态和重定向URL
            return jsonify({'success': True, 'redirectUrl': url_for('select_semester')})
        else:
            # 登录失败，返回错误信息
            logging.debug("登录失败：未找到匹配的凭据或密码错误")
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
    except mysql.connector.Error as err:
        # 数据库查询出错
        logging.error(f"数据库查询错误: {err}")
        return jsonify({'error': '服务错误，无法查询用户信息'}), 500
    finally:
        # 关闭数据库连接
        conn.close()


# 确保GET请求可以返回登录页面
@app.route('/login', methods=['GET'])
def login_form():
    """返回登录页面。"""
    return render_template('login.html')


@app.route('/logout')
def logout():
    """处理注销请求，清除会话。"""
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/select_semester', methods=['GET'])
def select_semester():
    """显示学期选择页面。"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT DISTINCT semester FROM class ORDER BY semester DESC")
        semesters = cursor.fetchall()
        return render_template('select_semester.html', semesters=semesters)
    except mysql.connector.Error as err:
        logging.error(f"数据库查询错误: {err}")
        return "Error fetching semesters from database", 500
    finally:
        conn.close()


@app.route('/api/courses', methods=['GET'])
def get_courses():
    semester = request.args.get('semester')
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
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
        courses = cursor.fetchall()
        return jsonify(courses)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/selected_courses', methods=['GET'])
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


@app.route('/list_courses', methods=['GET'])
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


@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    data = request.get_json()
    course_id = data['course_id']
    semester = data['semester']
    student_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO course_selection (student_id, course_id, semester) VALUES (%s, %s, %s)',
                       (student_id, course_id, semester))
        conn.commit()
        return jsonify({'success': True}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': str(err)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/drop_course', methods=['POST'])
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


@app.route('/favicon.ico')
def favicon():
    """提供网站图标。"""
    return app.send_static_file('favicon.ico')


if __name__ == '__main__':
    app.run(debug=True)
