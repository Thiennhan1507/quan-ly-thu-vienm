import tkinter as tk
from tkinter import messagebox
import pymysql

class TablesApp:
    def __init__(self):
        root = tk.Tk()
        root.title("Khởi tạo Cơ sở dữ liệu Thư viện")
        root.geometry("300x200")

        tk.Label(root, text="Khởi tạo CSDL Thư viện", font=("Arial", 14)).pack(pady=20)
        
        tk.Button(root, text="Tạo CSDL và Bảng", command=self.create_tables).pack(pady=10)
        tk.Button(root, text="Đóng", command=root.destroy).pack(pady=10)

        root.mainloop()

    def create_tables(self):
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="200511",
            database="Library",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor
        )
        mycursor = mydb.cursor()


        mycursor.execute("CREATE DATABASE IF NOT EXISTS Library")
        mycursor.execute("USE Library")

        # Bảng Sách
        mycursor.execute("SHOW TABLES LIKE 'BookRecord'")
        if not mycursor.fetchone():
            mycursor.execute("""
                CREATE TABLE BookRecord(
                    BookID varchar(10) PRIMARY KEY, 
                    BookName varchar(50), 
                    Author varchar(30), 
                    Publisher varchar(30)
                )
            """)

        # Bảng Người dùng
        mycursor.execute("SHOW TABLES LIKE 'UserRecord'")
        if not mycursor.fetchone():
            mycursor.execute("""
                CREATE TABLE UserRecord(
                    UserID varchar(20) PRIMARY KEY, 
                    UserName varchar(30) NOT NULL,
                    Passwd varchar(50) NOT NULL, 
                    BookID varchar(10), 
                    FOREIGN KEY (BookID) REFERENCES BookRecord(BookID) ON DELETE SET NULL ON UPDATE CASCADE
                )
            """)

        # Bảng Quản trị viên
        mycursor.execute("SHOW TABLES LIKE 'AdminRecord'")
        if not mycursor.fetchone():
            mycursor.execute("""
                CREATE TABLE AdminRecord(
                    AdminID varchar(10) PRIMARY KEY, 
                    Passwd varchar(20)
                )
            """)

        # Bảng Phản hồi
        mycursor.execute("SHOW TABLES LIKE 'Feedback'")
        if not mycursor.fetchone():
            mycursor.execute("""
                CREATE TABLE Feedback(
                    Feedback varchar(100) PRIMARY KEY, 
                    Feedback TEXT,         
                    Rating INT,
                    CONSTRAINT check_rating CHECK (Rating >= 0 AND Rating <= 10) 
                )
            """)

        messagebox.showinfo("Thành công", "Đã tạo thành công CSDL và các bảng.")

if __name__ == "__main__":
    app = TablesApp()
