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
        
        self.mydb = mysql.connector.connect(host="127.0.0.1", user="root", passwd="taolao", database="Library")
        self.mycursor = self.mydb.cursor()

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
        
        tk.Button(self.root, text="Add Book Record", command=Book.insertBook).pack(pady=10)
        tk.Button(self.root, text="Display Book Records", command=Book.displayBook).pack(pady=10)
        tk.Button(self.root, text="Search Book Record", command=Book.searchBook).pack(pady=10)
        tk.Button(self.root, text="Delete Book Record", command=Book.deleteBook).pack(pady=10)
        tk.Button(self.root, text="Update Book Record", command=Book.updateBook).pack(pady=10)
        tk.Button(self.root, text="Return to Main Menu", command=self.root.destroy).pack(pady=10)

    def user_management(self):
        tk.Label(self.root, text="User Record Management", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Add User Record", command=User.insertUser).pack(pady=10)
        tk.Button(self.root, text="Display User Records", command=User.displayUser).pack(pady=10)
        tk.Button(self.root, text="Search User Record", command=User.searchUser).pack(pady=10)
        tk.Button(self.root, text="Delete User Record", command=User.deleteUser).pack(pady=10)
        tk.Button(self.root, text="Update User Record", command=User.updateUser).pack(pady=10)
        tk.Button(self.root, text="Return to Main Menu", command=self.root.destroy).pack(pady=10)

    def admin_management(self):
        tk.Label(self.root, text="Admin Record Management", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Add Admin Record", command=Admin.insertAdmin).pack(pady=10)
        tk.Button(self.root, text="Display Admin Records", command=Admin.displayAdmin).pack(pady=10)
        tk.Button(self.root, text="Search Admin Record", command=Admin.searchAdmin).pack(pady=10)
        tk.Button(self.root, text="Delete Admin Record", command=Admin.deleteAdmin).pack(pady=10)
        tk.Button(self.root, text="Update Admin Record", command=Admin.updateAdmin).pack(pady=10)
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
        
        tk.Button(self.root, text="List of all Books", command=Book.BookList).pack(pady=10)
        tk.Button(self.root, text="Issue Book", command=Book.IssueBook).pack(pady=10)
        tk.Button(self.root, text="Display Issued Book Records", command=Book.ShowIssuedBook).pack(pady=10)
        tk.Button(self.root, text="Return Issued Book", command=Book.returnBook).pack(pady=10)
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
    root = tk.Tk()
    app = OperationsApp(root, "Book Management")
    root.mainloop()

def UserManagement():
    root = tk.Tk()
    app = OperationsApp(root, "User Management")
    root.mainloop()

def AdminManagement():
    root = tk.Tk()
    app = OperationsApp(root, "Admin Management")
    root.mainloop()

def FeedbackTable():
    root = tk.Tk()
    app = OperationsApp(root, "Feedback Table")
    root.mainloop()

def BookCentre():
    root = tk.Tk()
    app = OperationsApp(root, "Book Centre")
    root.mainloop()

def Feedback():
    root = tk.Tk()
    app = OperationsApp(root, "Feedback")
    root.mainloop()