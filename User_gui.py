import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import Tables_gui as Tables
class UserApp:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="localhost", user="root", passwd="200511", database="Library")
        self.mycursor = self.mydb.cursor()

    def displayUser(self):
        win = tk.Toplevel()
        win.title("Display User Records")
        win.geometry("500x400")

        tree = ttk.Treeview(win, columns=("UserID", "UserName", "Password", "BookName", "BookID"), show="headings")
        tree.heading("UserID", text="UserID")
        tree.heading("UserName", text="UserName")
        tree.heading("Password", text="Password")
        tree.heading("BookName", text="Book Issued")
        tree.heading("BookID", text="BookID")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""SELECT UserRecord.UserID, UserRecord.UserName, UserRecord.Password, 
                                BookRecord.BookName, BookRecord.BookID
                                FROM UserRecord LEFT JOIN BookRecord ON UserRecord.BookID=BookRecord.BookID""")
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def insertUser(self):
        win = tk.Toplevel()
        win.title("Add User Record")
        win.geometry("300x250")

        tk.Label(win, text="Add User", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="UserID:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        tk.Label(win, text="UserName:").pack()
        user_name_entry = tk.Entry(win)
        user_name_entry.pack()

        tk.Label(win, text="Password:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        def add_user():
            user_id = user_id_entry.get()
            user_name = user_name_entry.get()
            password = password_entry.get()
            if all([user_id, user_name, password]):
                query = "INSERT INTO UserRecord (UserID, UserName, Password, BookID) VALUES (%s, %s, %s, %s)"
                self.mycursor.execute(query, (user_id, user_name, password, None))
                self.mydb.commit()
                messagebox.showinfo("Success", "User added successfully")
                if not messagebox.askyesno("Continue", "Do you wish to add more Users?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(win, text="Add", command=add_user).pack(pady=10)

    def deleteUser(self):
        win = tk.Toplevel()
        win.title("Delete User Record")
        win.geometry("300x150")

        tk.Label(win, text="Delete User", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="UserID:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        def delete_user():
            user_id = user_id_entry.get()
            if user_id:
                self.mycursor.execute("DELETE FROM UserRecord WHERE UserID=%s", (user_id,))
                self.mydb.commit()
                messagebox.showinfo("Success", "User deleted successfully")
                if not messagebox.askyesno("Continue", "Do you wish to delete more Users?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please enter UserID")

        tk.Button(win, text="Delete", command=delete_user).pack(pady=10)

    def searchUser(self):
        win = tk.Toplevel()
        win.title("Search User Record")
        win.geometry("300x200")

        tk.Label(win, text="Search User", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="UserID:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        def search_user():
            user_id = user_id_entry.get()
            if user_id:
                self.mycursor.execute("""SELECT UserRecord.UserID, UserRecord.UserName, UserRecord.Password, 
                                        BookRecord.BookName, UserRecord.BookID
                                        FROM UserRecord LEFT JOIN BookRecord ON UserRecord.BookID=BookRecord.BookID
                                        WHERE UserRecord.UserID=%s""", (user_id,))
                records = self.mycursor.fetchall()
                if records:
                    result_win = tk.Toplevel()
                    result_win.title("Search Result")
                    result_win.geometry("400x200")
                    for row in records:
                        tk.Label(result_win, text=f"UserID: {row[0]}").pack()
                        tk.Label(result_win, text=f"UserName: {row[1]}").pack()
                        tk.Label(result_win, text=f"Password: {row[2]}").pack()
                        tk.Label(result_win, text=f"Book Issued: {row[3]}").pack()
                        tk.Label(result_win, text=f"BookID: {row[4]}").pack()
                    tk.Button(result_win, text="Close", command=result_win.destroy).pack(pady=10)
                else:
                    messagebox.showinfo("Result", "Search Unsuccessful")
                if not messagebox.askyesno("Continue", "Do you wish to search more Users?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please enter UserID")

        tk.Button(win, text="Search", command=search_user).pack(pady=10)

    def updateUser(self):
        win = tk.Toplevel()
        win.title("Update User Record")
        win.geometry("300x250")

        tk.Label(win, text="Update User", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="UserID:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        tk.Label(win, text="UserName:").pack()
        user_name_entry = tk.Entry(win)
        user_name_entry.pack()

        tk.Label(win, text="Password:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        def update_user():
            user_id = user_id_entry.get()
            user_name = user_name_entry.get()
            password = password_entry.get()
            if all([user_id, user_name, password]):
                query = "UPDATE UserRecord SET UserName=%s, Password=%s WHERE UserID=%s"
                self.mycursor.execute(query, (user_name, password, user_id))
                self.mydb.commit()
                messagebox.showinfo("Success", "User updated successfully")
                if not messagebox.askyesno("Continue", "Do you wish to update more Users?"):
                    win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        tk.Button(win, text="Update", command=update_user).pack(pady=10)