import pymysql

# Kết nối đến MySQL
mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="200511",
    database="Library",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.Cursor
)
mycursor = mydb.cursor()

# Tạo cơ sở dữ liệu "Library" nếu chưa tồn tại
mycursor.execute("CREATE DATABASE IF NOT EXISTS Library")
mycursor.execute("USE Library")

# Tạo bảng BookRecord nếu chưa tồn tại
mycursor.execute("SHOW TABLES LIKE 'BookRecord'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE BookRecord(
            BookID VARCHAR(10) PRIMARY KEY,
            BookName VARCHAR(35),
            Author VARCHAR(30),
            Publisher VARCHAR(30)
        )
    """)

# Tạo bảng UserRecord nếu chưa tồn tại
mycursor.execute("SHOW TABLES LIKE 'UserRecord'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE UserRecord(
            UserID VARCHAR(10) PRIMARY KEY,
            UserName VARCHAR(20),
            Password VARCHAR(20),
            BookID VARCHAR(10),
            FOREIGN KEY (BookID) REFERENCES BookRecord(BookID)
        )
    """)

# Tạo bảng AdminRecord nếu chưa tồn tại
mycursor.execute("SHOW TABLES LIKE 'AdminRecord'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE AdminRecord(
            AdminID VARCHAR(10) PRIMARY KEY,
            Passwd VARCHAR(20)
        )
    """)

# Tạo bảng Feedback nếu chưa tồn tại
mycursor.execute("SHOW TABLES LIKE 'Feedback'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE Feedback(
            Feedback VARCHAR(100) PRIMARY KEY,
            Rating VARCHAR(10)
        )
    """)
