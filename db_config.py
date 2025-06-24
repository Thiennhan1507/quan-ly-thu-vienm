# db_config.py
import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="200511",
        database="Library",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )
