import tkinter as tk
from tkinter import messagebox
import Operations_gui as Operations

class MainMenuApp:
    def __init__(self, root, role):
        self.root = root
        self.root.title("The Book Worm - Main Menu")
        self.root.geometry("400x300")
        self.role = role

        if self.role == "Admin":
            self.admin_menu()
        else:
            self.user_menu()

    def admin_menu(self):
        tk.Label(self.root, text="Admin Menu", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Book Management", command=Operations.BookManagement).pack(pady=10)
        tk.Button(self.root, text="User Management", command=Operations.UserManagement).pack(pady=10)
        tk.Button(self.root, text="Admin Management", command=Operations.AdminManagement).pack(pady=10)
        tk.Button(self.root, text="Feedback Table", command=Operations.FeedbackTable).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def user_menu(self):
        tk.Label(self.root, text="User Menu", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Book Centre", command=Operations.BookCentre).pack(pady=10)
        tk.Button(self.root, text="Feedback and Ratings", command=Operations.Feedback).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def logout(self):
        messagebox.showinfo("Logout", "Thanks for visiting our Library! Logged out.")
        self.root.destroy()

def Adminmenu():
    root = tk.Tk()
    app = MainMenuApp(root, "Admin")
    root.mainloop()

def Usermenu():
    root = tk.Tk()
    app = MainMenuApp(root, "User")
    root.mainloop()