from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import mysql.connector
from config.db_config import get_db_connection
from script.encrypt import update_passwords

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

@admin_bp.route('/api/update_course', methods=['POST'])
def update_course():
    data = request.get_json()
    course_id = data['course_id']
    course_name = data['course_name']
    credit = data['credit']
    credit_hours = data['credit_hours']
    dept_id=data['dept_id']
    print(course_id)
    print(course_name)
    print(credit)
    print(credit_hours)
    print(dept_id)

    # 构建更新 SQL 语句
    update_sql = """
    UPDATE course
    SET 
        course_name = %s,
        credit = %s,
        credit_hours = %s,
        dept_id = %s
    WHERE course_id = %s;
    """
    values = (
        data['course_name'],
        data['credit'],
        data['credit_hours'],
        data['dept_id'],
        course_id
    )
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(update_sql, values)
        conn.commit()
        return jsonify({'success': True, 'message': '课程信息更新成功'})
    except mysql.connector.Error as err:
        # 这里捕获由触发器引发的错误
        conn.rollback()
        return jsonify({'success': False, 'message': '更新失败: ' + str(err)})
    finally:
        cursor.close()
        conn.close()


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
    default_password = 'password' + data['student_id']
    encrypted_password = update_passwords(default_password)
    # 首先验证部门ID是否存在
    cursor.execute("SELECT 1 FROM department WHERE dept_id = %s", (data['dept_id'],))
    if cursor.fetchone() is None:
        return jsonify({'success': False, 'message': '指定的部门ID不存在'}), 400

    try:
        sql = "INSERT INTO student (student_id, name, sex, date_of_birth, native_place, mobile_phone, dept_id, Status, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            data['student_id'],
            data['name'],
            data['sex'],
            data['date_of_birth'],
            data['native_place'],
            data['mobile_phone'],
            data['dept_id'],
            data['Status'],
            encrypted_password
        ))
        conn.commit()
        return jsonify({'success': True, 'message': '学生添加成功'})
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': '数据库错误: ' + str(err)})
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

@admin_bp.route('/api/update_student_password', methods=['POST'])
def update_student_password():
    data = request.get_json()
    student_id = data['student_id']
    new_password = data['new_password']
    # 更新数据库逻辑
    encrypted_password = update_passwords(new_password)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE student
            SET password = %s
            WHERE student_id = %s
        """, (encrypted_password, student_id))
        conn.commit()
        return jsonify({'success': True, 'message': '密码更新成功'})
    except Exception as e:
        conn.rollback()
        print("Error updating grade:", e)
        return jsonify({'success': False, 'message': str(e)})
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
    default_password = 'password' + data['staff_id']
    encrypted_password = update_passwords(default_password)
    # 首先验证部门ID是否存在
    cursor.execute("SELECT 1 FROM department WHERE dept_id = %s", (data['dept_id'],))
    if cursor.fetchone() is None:
        return jsonify({'success': False, 'message': '指定的部门ID不存在'}), 400

    try:
        sql = "INSERT INTO teacher (staff_id, name, sex, date_of_birth, professional_ranks, salary, dept_id, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            data['staff_id'],
            data['name'],
            data['sex'],
            data['date_of_birth'],
            data['professional_ranks'],
            data['salary'],
            data['dept_id'],
            encrypted_password
        ))

        conn.commit()

        return jsonify({'success': True, 'message': '教师添加成功'})
    except mysql.connector.Error as err:
        conn.rollback()
        print(str(err))
        return jsonify({'success': False, 'message': '数据库错误: ' + str(err)})
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

@admin_bp.route('/api/update_dept', methods=['POST'])
def update_dept():
    data = request.get_json()
    dept_id = data['dept_id']
    dept_name = data['dept_name']
    address = data['address']
    phone_code = data['phone_code']

    # 输出日志以方便调试
    print(dept_id, dept_name, address, phone_code)

    # 构建更新SQL语句
    update_sql = """
    UPDATE department
    SET 
        dept_name = %s,
        address = %s,
        phone_code = %s
    WHERE dept_id = %s;
    """
    values = (
        dept_name,
        address,
        phone_code,
        dept_id
    )

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(update_sql, values)
        conn.commit()

        return jsonify({'success': True, 'message': '院系信息更新成功'})
    except mysql.connector.Error as err:
        # 这里捕获由触发器引发的错误
        conn.rollback()
        return jsonify({'success': False, 'message': '更新失败: ' + str(err)})
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

@admin_bp.route('/api/add_cll', methods=['POST'])
def add_cll():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 首先检查是否已存在相同的课程组合
        check_sql = """
            SELECT COUNT(*) FROM class
            WHERE semester = %s AND course_id = %s AND staff_id = %s
        """
        cursor.execute(check_sql, (data['semester'], data['course_id'], data['staff_id']))
        if cursor.fetchone()[0] > 0:
            return jsonify({'success': False, 'message': '添加失败：相同的课程组合已存在'}), 400

        # 如果检查通过，则插入新课程
        insert_sql = """
            INSERT INTO class (class_id, semester, course_id, staff_id, class_time)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (
            data['class_id'],
            data['semester'],
            data['course_id'],
            data['staff_id'],
            data['class_time']
        ))
        conn.commit()
        return jsonify({'success': True, 'message': '课程添加成功'})
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'success': False, 'message': '数据库错误: ' + str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@admin_bp.route('/api/delete_cll/<class_id>', methods=['DELETE'])
def delete_cll(class_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 先查询相应的semester, course_id, staff_id
        cursor.execute("SELECT semester, course_id, staff_id FROM class WHERE class_id = %s", (class_id,))
        class_info = cursor.fetchone()

        if class_info is None:
            return jsonify({'success': False, 'message': '未找到指定的课程'}), 404

        semester, course_id, staff_id = class_info

        # 检查course_selection表中是否存在记录
        cursor.execute("""
            SELECT COUNT(*) FROM course_selection 
            WHERE semester = %s AND course_id = %s AND staff_id = %s
            """, (semester, course_id, staff_id))
        selection_count = cursor.fetchone()[0]

        if selection_count > 0:
            return jsonify({'success': False, 'message': '无法删除，因为已有学生选择了此课程'}), 403

        # 如果未选课程，则尝试删除课程
        cursor.execute("DELETE FROM class WHERE class_id = %s", (class_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '课程删除成功'})

    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': '删除课程时发生错误: {}'.format(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/api/update_cll', methods=['POST'])
def update_cll():
    data = request.get_json()
    class_id = data['class_id']
    semester = data['semester']
    course_id = data['course_id']
    staff_id = data['staff_id']
    class_time = data['class_time']
    print(class_id)
    print(semester)
    print(course_id)
    print(staff_id)
    print(class_time)

    # 构建更新 SQL 语句
    update_sql = """
    UPDATE class
    SET 
        semester = %s,
        course_id = %s,
        staff_id = %s,
        class_time = %s
    WHERE class_id = %s;
    """
    values = (
        semester,
        course_id,
        staff_id,
        class_time,
        class_id
    )
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(update_sql, values)
        conn.commit()
        return jsonify({'success': True, 'message': '课程信息更新成功'})
    except mysql.connector.Error as err:
        # 这里捕获由触发器引发的错误
        conn.rollback()
        return jsonify({'success': False, 'message': '更新失败: ' + str(err)})
    finally:
        cursor.close()
        conn.close()

# Add this endpoint definition under the admin_bp blueprint
@admin_bp.route('/cll_list')
def cll_list():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql_query = """
        SELECT class_id, semester, c.course_id, c.course_name, staff_id, class_time
        FROM class cl
        join course c on c.course_id = cl.course_id
        WHERE class_id LIKE %s OR c.course_id LIKE %s OR staff_id like %s OR class_time like %s OR course_name like %s
        """
    cursor.execute(sql_query, ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    clls = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clls=clls)




#测试中开课功能
'''
@admin_bp.route('/check_class_id', methods=['POST'])
def check_class_id():
    # 检查请求中是否有JSON数据
    if not request.json:
        return jsonify({'error': 'Bad Request', 'message': 'No JSON data provided'}), 400

    class_id = request.json.get('class_id')
    if not class_id:
        return jsonify({'error': 'Bad Request', 'message': 'Missing class_id in JSON data'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM class WHERE class_id = %s)", (class_id,))
    exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return jsonify({'exists': bool(exists)})

@admin_bp.route('/search_courses', methods=['GET'])
def search_courses():
    query = request.args.get('query', '')
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT course_id, course_name FROM course
        WHERE course_id LIKE %s OR course_name LIKE %s
        """, ('%' + query + '%', '%' + query + '%'))
    courses = cur.fetchall()
    cur.close()
    return jsonify({'courses': [{'course_id': row[0], 'course_name': row[1]} for row in courses]})


@admin_bp.route('/search_teachers', methods=['GET'])
def search_teachers():
    query = request.args.get('query')
    course_id = request.args.get('course_id')
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT t.staff_id, t.name FROM teacher t
        JOIN course c ON t.dept_id = c.dept_id
        WHERE (t.name LIKE %s OR t.staff_id LIKE %s) AND c.course_id = %s
        """, ('%' + query + '%', '%' + query + '%', course_id))
    teachers = cur.fetchall()
    cur.close()
    return jsonify({'teachers': [{'staff_id': row[0], 'name': row[1]} for row in teachers]})

@admin_bp.route('/add_class', methods=['POST'])
def add_class():
    data = request.get_json()
    class_id = data['class_id']
    semester = data['semester']
    course_id = data['course_id']
    staff_id = data['staff_id']
    class_time = data['class_time']
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO class (class_id, semester, course_id, staff_id, class_time)
            VALUES (%s, %s, %s, %s, %s)
            """, (class_id, semester, course_id, staff_id, class_time))
        mysql.connection.commit()
        return jsonify({'success': True, 'message': '课程已成功添加'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cur.close()
'''


@admin_bp.route('/api/edit_student', methods=['PUT'])
def edit_student():
    data = request.get_json()
    student_id = data['student_id']
    name = data.get('name')  # 使用get方法以允许字段为None
    sex = data.get('sex')
    date_of_birth = data.get('date_of_birth')
    native_place = data.get('native_place')
    mobile_phone = data.get('mobile_phone')
    dept_id = data.get('dept_id')
    status = data.get('status')  # 注意：Status字段通常应小写化
    password = data.get('password')

    # 使用自定义的数据库连接函数
    conn = get_db_connection()
    cur = conn.cursor()

    # 验证学生ID是否存在
    cur.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
    student_exists = cur.fetchone()
    if not student_exists:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'message': '学生ID不存在'})

    update_fields = []
    values = []
    for field in ['name', 'sex', 'date_of_birth', 'native_place', 'mobile_phone', 'dept_id', 'status', 'password']:
        if locals()[field] is not None:  # 检查字段是否有值
            update_fields.append(f"{field} = %s")
            values.append(locals()[field])

    # 构建UPDATE语句
    update_query = "UPDATE student SET " + ", ".join(update_fields) + " WHERE student_id = %s"
    values.append(student_id)

    try:
        cur.execute(update_query, values)
        conn.commit()
        return jsonify({'success': True, 'message': '学生信息已成功更新'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cur.close()
        conn.close()

@admin_bp.route('/api/edit_teacher', methods=['PUT'])
def edit_teacher():
    data = request.get_json()
    staff_id = data.get('staff_id')
    name = data.get('name')
    sex = data.get('sex')
    date_of_birth = data.get('date_of_birth')
    professional_ranks = data.get('professional_ranks')
    salary = data.get('salary')
    dept_id = data.get('dept_id')

    # 使用自定义的数据库连接函数
    conn = get_db_connection()
    cur = conn.cursor()

    # 构建更新语句
    update_fields = []
    values = []
    for field in ['name', 'sex', 'date_of_birth', 'professional_ranks', 'salary', 'dept_id']:
        value = locals()[field]
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)

    if update_fields:
        update_query = f"UPDATE teacher SET {', '.join(update_fields)} WHERE staff_id = %s"
        values.append(staff_id)

        try:
            cur.execute(update_query, values)
            conn.commit()
            return jsonify({'success': True, 'message': '教师信息已成功更新'})
        except Exception as e:
            conn.rollback()
            return jsonify({'success': False, 'message': str(e)})
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({'success': False, 'message': '无更新的数据'})






