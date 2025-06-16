import tkinter as tk
from tkinter import messagebox
import mysql.connector

class TablesApp:
    def __init__(self):
        root = tk.Tk()
        root.title("Initialize Database")
        root.geometry("300x200")

        tk.Label(root, text="Initialize Library Database", font=("Arial", 14)).pack(pady=20)
        
        tk.Button(root, text="Create Database and Tables", command=self.create_tables).pack(pady=10)
        tk.Button(root, text="Close", command=root.destroy).pack(pady=10)

        root.mainloop()

    def create_tables(self):
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="200511")
        mycursor = mydb.cursor()
        
        mycursor.execute("CREATE DATABASE IF NOT EXISTS Library")
        mycursor.execute("USE Library")

        # Tạo bảng BookRecord
        mycursor.execute("SHOW TABLES LIKE 'BookRecord'")
        if not mycursor.fetchone():
            mycursor.execute("""CREATE TABLE BookRecord(BookID varchar(10) PRIMARY KEY, 
                            BookName varchar(35), Author varchar(30), Publisher varchar(30))""")

        # Tạo bảng UserRecord
        mycursor.execute("SHOW TABLES LIKE 'UserRecord'")
        if not mycursor.fetchone():
            mycursor.execute("""CREATE TABLE UserRecord(UserID varchar(10) PRIMARY KEY, UserName varchar(20),
                            Password varchar(20), BookID varchar(10), FOREIGN KEY (BookID) REFERENCES BookRecord(BookID))""")
            data1 = ("101", "Kunal", "1234", None)
            data2 = ("102", "Vishal", "3050", None)
            data3 = ("103", "Siddhesh", "5010", None)
            query = "INSERT INTO UserRecord VALUES (%s, %s, %s, %s)"
            mycursor.execute(query, data1)
            mycursor.execute(query, data2)
            mycursor.execute(query, data3)
            mydb.commit()

        # Tạo bảng AdminRecord
        mycursor.execute("SHOW TABLES LIKE 'AdminRecord'")
        if not mycursor.fetchone():
            mycursor.execute("""CREATE TABLE AdminRecord(AdminID varchar(10) PRIMARY KEY, Password varchar(20))""")
            data4 = ("Kunal1020", "123")
            data5 = ("Siddesh510", "786")
            data6 = ("Vishal305", "675")
            query = "INSERT INTO AdminRecord VALUES (%s, %s)"
            mycursor.execute(query, data4)
            mycursor.execute(query, data5)
            mycursor.execute(query, data6)
            mydb.commit()

        # Tạo bảng Feedback
        mycursor.execute("SHOW TABLES LIKE 'Feedback'")
        if not mycursor.fetchone():
            mycursor.execute("""CREATE TABLE Feedback(Feedback varchar(100) PRIMARY KEY, Rating varchar(10))""")

        messagebox.showinfo("Success", "Database and tables created successfully")

if __name__ == "__main__":
    app = TablesApp()