import mysql.connector

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
