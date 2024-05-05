from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import mysql.connector
import bcrypt
import logging
from config.db_config import conn_params
from teacher.teacher_routes import teacher_bp
from student.student_routes import student_bp
from admin.admin_routes import admin_bp

app = Flask(__name__)
app.secret_key = 'yhempr666'
logging.basicConfig(level=logging.DEBUG)
app.register_blueprint(teacher_bp, url_prefix='/teacher')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(admin_bp, url_prefix='/admin')


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
    if 'user_id' not in session or 'role' not in session or session['role'] != 'teacher':
        logging.debug("未认证的用户访问或角色不正确")
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 假设有一个表class_teachers关联教师和他们教的课程以及学期信息
        cursor.execute("""
            SELECT distinct c.course_id, c.course_name, ct.semester, ct.staff_id
            FROM class as ct
            JOIN course as c ON ct.course_id = c.course_id
            WHERE ct.staff_id = %s
            ORDER BY ct.semester DESC
        """, (user_id,))
        courses = cursor.fetchall()
        return render_template('teacher_home.html', courses=courses)
    except Exception as err:  # 捕捉更一般的异常，例如数据库连接失败
        logging.error(f"数据库查询错误: {err}")
        return "Error fetching courses from database", 500
    finally:
        cursor.close()
        conn.close()


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
    """
    处理用户登录请求。

    接收JSON格式的用户ID、密码和角色信息，验证用户身份并根据角色重定向到相应的首页。

    参数:
    - 无

    返回值:
    - 成功登录: 包含成功标志和重定向URL的JSON对象
    - 登录失败: 包含成功标志和错误消息的JSON对象

    错误码:
    - 400: 无效的请求或缺少必要参数
    - 401: 用户名或密码错误
    - 500: 服务错误，无法查询用户信息
    """
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





@app.route('/favicon.ico')
def favicon():
    """提供网站图标。"""
    return app.send_static_file('favicon.ico')


if __name__ == '__main__':
    app.run(debug=True)
