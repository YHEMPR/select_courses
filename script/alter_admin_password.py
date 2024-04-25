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

# 更新数据库中的管理员密码
def update_admin_passwords():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取所有管理员的明文密码
    cursor.execute("SELECT admin_id, admin_password FROM admin")
    admins = cursor.fetchall()

    for admin_id, plain_password in admins:
        hashed_password = hash_password(plain_password)

        # 更新管理员的密码
        cursor.execute("UPDATE admin SET admin_password = %s WHERE admin_id = %s", (hashed_password, admin_id))

    conn.commit()  # 提交事务
    cursor.close()
    conn.close()
    print("所有管理员密码已更新为加密格式。")

if __name__ == "__main__":
    update_admin_passwords()
