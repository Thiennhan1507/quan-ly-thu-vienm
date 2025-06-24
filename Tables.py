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
            BookID varchar(10) PRIMARY KEY, 
            BookName varchar(50), 
            Author varchar(30), 
            Publisher varchar(30)
        )
    """)

# Tạo bảng UserRecord nếu chưa tồn tại
mycursor.execute("SHOW TABLES LIKE 'UserRecord'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE UserRecord(
            UserID varchar(20) PRIMARY KEY, 
            UserName varchar(30) NOT NULL,
            Passwd varchar(50) NOT NULL, 
            BookID varchar(10), 
            FOREIGN KEY (BookID) REFERENCES BookRecord(BookID) ON DELETE SET NULL ON UPDATE CASCADE
        )
    """)

# Tạo bảng AdminRecord nếu chưa tồn tại
mycursor.execute("SHOW TABLES LIKE 'AdminRecord'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE AdminRecord(
            AdminID VARCHAR(10) PRIMARY KEY,
            Password VARCHAR(20)
        )
    """)

# Tạo bảng Feedback nếu chưa tồn tại
mycursor.execute("SHOW TABLES LIKE 'Feedback'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE Feedback(
            Feedback varchar(100) PRIMARY KEY, 
            Feedback TEXT,         
            Rating INT,
            CONSTRAINT check_rating CHECK (Rating >= 0 AND Rating <= 10) 
        )
    """)
