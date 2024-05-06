import mysql.connector
import bcrypt

# 数据库连接参数
db_config = {
    'user': 'root',
    'password': '1Faqnig1',
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
def update_passwords(plain_password):
    hashed_password = hash_password(plain_password)
    return hashed_password
if __name__ == "__main__":
    update_passwords()
