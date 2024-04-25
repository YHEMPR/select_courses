import mysql.connector
import bcrypt

# 数据库连接参数
db_config = {
    'user': 'root',
    'password': '5201314Eminem',  # 请确保使用安全的方式处理密码
    'host': 'localhost',
    'database': 'school',
    'auth_plugin': 'mysql_native_password'
}

# 连接数据库
def get_db_connection():
    """创建并返回数据库连接"""
    return mysql.connector.connect(**db_config)

# 生成哈希密码
def hash_password(password):
    """使用 bcrypt 哈希密码"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

# 更新数据库中的老师密码
def update_teacher_passwords():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取所有老师的明文密码
    cursor.execute("SELECT staff_id, password FROM teacher")
    teachers = cursor.fetchall()

    for staff_id, plain_password in teachers:
        hashed_password = hash_password(plain_password)

        # 更新老师的密码
        cursor.execute("UPDATE teacher SET password = %s WHERE staff_id = %s", (hashed_password, staff_id))

    conn.commit()  # 提交事务
    cursor.close()
    conn.close()
    print("所有老师密码已更新为加密格式。")

if __name__ == "__main__":
    update_teacher_passwords()
