import mysql.connector
import bcrypt

# 数据库连接参数
db_config = {
    'user': 'root',
    'password': '5201314Eminem',
    'host': 'localhost',
    'database': 'school',
    'auth_plugin': 'mysql_native_password'
}

# 连接数据库
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 生成哈希密码
def hash_password(password):
    """使用 bcrypt 哈希密码"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

# 更新数据库中的密码
def update_passwords():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取所有学生的明文密码
    cursor.execute("SELECT student_id, password FROM student")
    students = cursor.fetchall()

    for student_id, plain_password in students:
        hashed_password = hash_password(plain_password)

        # 更新学生的密码
        cursor.execute("UPDATE student SET password = %s WHERE student_id = %s", (hashed_password, student_id))

    conn.commit()  # 提交事务
    cursor.close()
    conn.close()
    print("所有密码已更新为加密格式。")

if __name__ == "__main__":
    update_passwords()
