import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import Book_gui as Book
import User_gui as User
import Admin_gui as Admin
import Tables_gui as Tables

class OperationsApp:
    def __init__(self, root, menu_type):
        self.root = root
        self.root.title(f"The Book Worm - {menu_type}")
        self.root.geometry("400x400")
        self.menu_type = menu_type

        # Kết nối DB và khởi tạo các app thành viên
        self.mydb = mysql.connector.connect(host="127.0.0.1", user="root", passwd="taolao", database="Library")
        self.mycursor = self.mydb.cursor()

        self.book_app = Book.BookApp()
        self.user_app = User.UserApp()
        self.admin_app = Admin.AdminApp()

        if menu_type == "Book Management":
            self.book_management()
        elif menu_type == "User Management":
            self.user_management()
        elif menu_type == "Admin Management":
            self.admin_management()
        elif menu_type == "Feedback Table":
            self.feedback_table()
        elif menu_type == "Book Centre":
            self.book_centre()
        elif menu_type == "Feedback":
            self.feedback()

    def book_management(self):
        tk.Label(self.root, text="Book Record Management", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Add Book Record", command=self.book_app.insertBook).pack(pady=10)
        tk.Button(self.root, text="Display Book Records", command=self.book_app.displayBook).pack(pady=10)
        tk.Button(self.root, text="Search Book Record", command=self.book_app.searchBook).pack(pady=10)
        tk.Button(self.root, text="Delete Book Record", command=self.book_app.deleteBook).pack(pady=10)
        tk.Button(self.root, text="Update Book Record", command=self.book_app.updateBook).pack(pady=10)
        tk.Button(self.root, text="Return to Main Menu", command=self.root.destroy).pack(pady=10)

    def user_management(self):
        tk.Label(self.root, text="User Record Management", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Add User Record", command=self.user_app.insertUser).pack(pady=10)
        tk.Button(self.root, text="Display User Records", command=self.user_app.displayUser).pack(pady=10)
        tk.Button(self.root, text="Search User Record", command=self.user_app.searchUser).pack(pady=10)
        tk.Button(self.root, text="Delete User Record", command=self.user_app.deleteUser).pack(pady=10)
        tk.Button(self.root, text="Update User Record", command=self.user_app.updateUser).pack(pady=10)
        tk.Button(self.root, text="Return to Main Menu", command=self.root.destroy).pack(pady=10)

    def admin_management(self):
        tk.Label(self.root, text="Admin Record Management", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Add Admin Record", command=self.admin_app.insertAdmin).pack(pady=10)
        tk.Button(self.root, text="Display Admin Records", command=self.admin_app.displayAdmin).pack(pady=10)
        tk.Button(self.root, text="Search Admin Record", command=self.admin_app.searchAdmin).pack(pady=10)
        tk.Button(self.root, text="Delete Admin Record", command=self.admin_app.deleteAdmin).pack(pady=10)
        tk.Button(self.root, text="Update Admin Record", command=self.admin_app.updateAdmin).pack(pady=10)
        tk.Button(self.root, text="Return to Main Menu", command=self.root.destroy).pack(pady=10)

    def feedback_table(self):
        tk.Label(self.root, text="Feedback and Rating Table", font=("Arial", 16)).pack(pady=20)
        tree = ttk.Treeview(self.root, columns=("Feedback", "Rating"), show="headings")
        tree.heading("Feedback", text="Feedback")
        tree.heading("Rating", text="Rating")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("SELECT * FROM Feedback")
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(self.root, text="Return to Main Menu", command=self.root.destroy).pack(pady=10)

    def book_centre(self):
        tk.Label(self.root, text="Book Centre", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="List of all Books", command=self.book_app.BookList).pack(pady=10)
        tk.Button(self.root, text="Issue Book", command=self.book_app.IssueBook).pack(pady=10)
        tk.Button(self.root, text="Display Issued Book Records", command=self.book_app.ShowIssuedBook).pack(pady=10)
        tk.Button(self.root, text="Return Issued Book", command=self.book_app.returnBook).pack(pady=10)
        tk.Button(self.root, text="Return to Main Menu", command=self.root.destroy).pack(pady=10)

    def feedback(self):
        feedback_win = tk.Toplevel(self.root)
        feedback_win.title("Feedback and Rating")
        feedback_win.geometry("400x300")

        tk.Label(feedback_win, text="Feedback and Rating", font=("Arial", 14)).pack(pady=10)
        tk.Label(feedback_win, text="Enter your Review:").pack()
        feedback_entry = tk.Text(feedback_win, height=5, width=30)
        feedback_entry.pack()

        tk.Label(feedback_win, text="Rate us out of 10:").pack()
        rating_entry = tk.Entry(feedback_win)
        rating_entry.pack()

        def submit_feedback():
            feedback = feedback_entry.get("1.0", tk.END).strip()
            rating = rating_entry.get()
            if feedback and rating:
                query = "INSERT INTO Feedback (Feedback, Rating) VALUES (%s, %s)"
                self.mycursor.execute(query, (feedback, rating))
                self.mydb.commit()
                messagebox.showinfo("Success", "Thank you for your valuable Feedback")
                feedback_win.destroy()
            else:
                messagebox.showerror("Error", "Please fill in both fields")

        tk.Button(feedback_win, text="Submit", command=submit_feedback).pack(pady=10)


def BookManagement():
    win = tk.Toplevel()
    OperationsApp(win, "Book Management")

def UserManagement():
    win = tk.Toplevel()
    OperationsApp(win, "User Management")

def AdminManagement():
    win = tk.Toplevel()
    OperationsApp(win, "Admin Management")

def FeedbackTable():
    win = tk.Toplevel()
    OperationsApp(win, "Feedback Table")

def BookCentre():
    win = tk.Toplevel()
    OperationsApp(win, "Book Centre")

def Feedback():
    win = tk.Toplevel()
    OperationsApp(win, "Feedback")
