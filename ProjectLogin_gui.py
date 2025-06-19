import tkinter as tk
from tkinter import messagebox
import mysql.connector
import MainMenu_gui as MainMenu  
import Tables_gui as Tables

class LibraryLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Book Worm - Login")
        self.root.geometry("400x300")
        
        # Kết nối database
        self.mydb = mysql.connector.connect(host="127.0.0.1", user="root", passwd="taolao", database="Library")
        self.mycursor = self.mydb.cursor()

        # Giao diện chính
        self.label = tk.Label(root, text="Welcome to The Book Worm", font=("Arial", 16))
        self.label.pack(pady=20)

        self.admin_button = tk.Button(root, text="Login as Admin", command=self.admin_login_window)
        self.admin_button.pack(pady=10)

        self.user_button = tk.Button(root, text="Login as User", command=self.user_login_window)
        self.user_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

    def admin_login_window(self):
        self.admin_win = tk.Toplevel(self.root)
        self.admin_win.title("Admin Login")
        self.admin_win.geometry("300x200")

        tk.Label(self.admin_win, text="Admin Login", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.admin_win, text="AdminID:").pack()
        self.admin_id_entry = tk.Entry(self.admin_win)
        self.admin_id_entry.pack()

        tk.Label(self.admin_win, text="Password:").pack()
        self.admin_pass_entry = tk.Entry(self.admin_win, show="*")
        self.admin_pass_entry.pack()

        tk.Button(self.admin_win, text="Login", command=self.admin_login).pack(pady=10)
        self.attempts = 3
        self.attempt_label = tk.Label(self.admin_win, text=f"Attempts left: {self.attempts}")
        self.attempt_label.pack()

    def admin_login(self):
        admin_id = self.admin_id_entry.get()
        password = self.admin_pass_entry.get()
        
        self.mycursor.execute("SELECT Password FROM AdminRecord WHERE AdminID=%s", (admin_id,))
        result = self.mycursor.fetchone()
        
        if result and result[0] == password:
            messagebox.showinfo("Success", f"Welcome {admin_id} to The Book Worm")
            self.admin_win.destroy()
            MainMenu.Adminmenu()  # Gọi menu Admin
        else:
            self.attempts -= 1
            self.attempt_label.config(text=f"Attempts left: {self.attempts}")
            messagebox.showerror("Error", "Invalid AdminID or Password")
            if self.attempts == 0:
                messagebox.showerror("Error", "Too many failed attempts. System off.")
                self.admin_win.destroy()
                self.root.destroy()

    def user_login_window(self):
        self.user_win = tk.Toplevel(self.root)
        self.user_win.title("User Login")
        self.user_win.geometry("300x200")

        tk.Label(self.user_win, text="User Login", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.user_win, text="Create Account", command=self.create_account_window).pack(pady=5)
        tk.Button(self.user_win, text="Login", command=self.user_login_form).pack(pady=5)

    def create_account_window(self):
        self.create_win = tk.Toplevel(self.user_win)
        self.create_win.title("Create User Account")
        self.create_win.geometry("300x250")

        tk.Label(self.create_win, text="Create Account", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.create_win, text="UserID:").pack()
        self.user_id_entry = tk.Entry(self.create_win)
        self.user_id_entry.pack()

        tk.Label(self.create_win, text="UserName:").pack()
        self.user_name_entry = tk.Entry(self.create_win)
        self.user_name_entry.pack()

        tk.Label(self.create_win, text="Password:").pack()
        self.user_pass_entry = tk.Entry(self.create_win, show="*")
        self.user_pass_entry.pack()

        tk.Button(self.create_win, text="Create", command=self.create_account).pack(pady=10)

    def create_account(self):
        user_id = self.user_id_entry.get()
        user_name = self.user_name_entry.get()
        password = self.user_pass_entry.get()

        self.mycursor.execute("SELECT UserID FROM UserRecord WHERE UserID=%s", (user_id,))
        result = self.mycursor.fetchone()
        if result:
            messagebox.showerror("Error", "Account already exists")
        else:
            query = "INSERT INTO UserRecord (UserID, UserName, Password, BookID) VALUES (%s, %s, %s, %s)"
            self.mycursor.execute(query, (user_id, user_name, password, None))
            self.mydb.commit()
            messagebox.showinfo("Success", "Account successfully created")
            self.create_win.destroy()

    def user_login_form(self):
        self.login_win = tk.Toplevel(self.user_win)
        self.login_win.title("User Login")
        self.login_win.geometry("300x200")

        tk.Label(self.login_win, text="User Login", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.login_win, text="UserID:").pack()
        self.user_id_login_entry = tk.Entry(self.login_win)
        self.user_id_login_entry.pack()

        tk.Label(self.login_win, text="Password:").pack()
        self.user_pass_login_entry = tk.Entry(self.login_win, show="*")
        self.user_pass_login_entry.pack()

        tk.Button(self.login_win, text="Login", command=self.user_login).pack(pady=10)
        self.attempts = 3
        self.attempt_label = tk.Label(self.login_win, text=f"Attempts left: {self.attempts}")
        self.attempt_label.pack()

    def user_login(self):
        user_id = self.user_id_login_entry.get()
        password = self.user_pass_login_entry.get()
        
        self.mycursor.execute("SELECT Password FROM UserRecord WHERE UserID=%s", (user_id,))
        result = self.mycursor.fetchone()
        
        if result and result[0] == password:
            messagebox.showinfo("Success", f"Welcome {user_id} to The Book Worm")
            self.login_win.destroy()
            MainMenu.Usermenu()  # Gọi menu User
        else:
            self.attempts -= 1
            self.attempt_label.config(text=f"Attempts left: {self.attempts}")
            messagebox.showerror("Error", "Invalid UserID or Password")
            if self.attempts == 0:
                messagebox.showerror("Error", "Too many failed attempts. System off.")
                self.login_win.destroy()
                self.root.destroy()

    def exit_program(self):
        if messagebox.askyesno("Exit", "Do you wish to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryLoginApp(root)
    root.mainloop()