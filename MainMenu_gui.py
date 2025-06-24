import tkinter as tk
from tkinter import messagebox
import Operations_gui as Operations
from Book_gui import BookApp
class MainMenuApp:
    def __init__(self, root, role):
        self.root = root
        self.root.title("Thư viện - Giao diện chính")
        self.root.geometry("400x300")
        self.role = role

        if self.role == "Admin":
            self.menu_admin()
        else:
            self.menu_nguoi_dung()

    def menu_admin(self):
        tk.Label(self.root, text="Giao diện Quản trị viên", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Quản lý sách", command=Operations.BookManagement).pack(pady=10)
        tk.Button(self.root, text="Quản lý người dùng", command=Operations.UserManagement).pack(pady=10)
        tk.Button(self.root, text="Quản lý quản trị viên", command=Operations.AdminManagement).pack(pady=10)
        tk.Button(self.root, text="Bảng phản hồi", command=Operations.FeedbackTable).pack(pady=10)
        tk.Button(self.root, text="Đăng xuất", command=self.dang_xuat).pack(pady=10)

    def menu_nguoi_dung(self):
        tk.Label(self.root, text="Giao diện Người dùng", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Trung tâm sách", command=Operations.BookCentre).pack(pady=10)
        tk.Button(self.root, text="Góp ý và đánh giá", command=Operations.Feedback).pack(pady=10)
        tk.Button(self.root, text="Đăng xuất", command=self.dang_xuat).pack(pady=10)

    def dang_xuat(self):
        messagebox.showinfo("Đăng xuất", "Cảm ơn bạn đã sử dụng thư viện! Đã đăng xuất.")
        self.root.destroy()

def Adminmenu():
    root = tk.Tk()
    app = MainMenuApp(root, "Admin")
    root.mainloop()

def Usermenu():
    root = tk.Tk()
    app = MainMenuApp(root, "User")
    root.mainloop()

root = tk.TK()
root.title("Hệ thống thư viện")

book_app = BookApp(root)

root.mainloop()