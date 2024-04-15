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

from flask import render_template


@app.route('/student_home')
def student_home():
    """学生的主页面"""
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
        cursor.close()
        conn.close()


@app.route('/teacher_home')
def teacher_home():
    """教师的主页面"""
    return render_template('teacher_home.html')


@app.route('/admin_home')
def admin_home():
    """管理员的主页面"""
    return render_template('admin_home.html')


@app.route('/')
def index():
    """重定向到登录页面。"""
    return redirect(url_for('login'))



@app.route('/login', methods=['POST'])
def login():
    """处理登录请求。"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '无效的请求'}), 400

    user_id = data.get('user_id')
    password = data.get('password')
    role = data.get('role')  # 获取角色信息

    if not user_id or not password or not role:
        return jsonify({'success': False, 'message': '缺少必要的参数'}), 400

    # 根据角色决定使用哪个字段名和表名
    role_to_table = {
        'student': ('student', 'student_id'),
        'teacher': ('teacher', 'staff_id'),
        'admin': ('admin', 'admin_id')
    }

    table_name, id_field = role_to_table.get(role, (None, None))
    if not table_name:
        return jsonify({'success': False, 'message': '无效的角色'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 构建并执行SQL查询
        query = f'SELECT * FROM {table_name} WHERE {id_field} = %s'
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        # 验证密码并设置session
        if user and check_password(user['password'], password):
            session['user_id'] = user_id
            session['role'] = role
            logging.debug(f"登录成功，正在重定向到{role}的首页")
            redirect_url = url_for(f'{role}_home')
            return jsonify({'success': True, 'redirectUrl': redirect_url})
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
    except mysql.connector.Error as err:
        logging.error(f"数据库查询错误: {err}")
        return jsonify({'error': '服务错误，无法查询用户信息'}), 500
    finally:
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
