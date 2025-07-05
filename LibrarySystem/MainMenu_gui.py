import tkinter as tk
from tkinter import messagebox, ttk
import Operations_gui as Operations
from library import get_top_borrowed_books, get_unreturned_books
from db_config import get_connection

# Thống kê sách mượn nhiều nhất
def show_top_borrowed_books():
    data = get_top_borrowed_books()

    win = tk.Toplevel()
    win.title("Thống kê sách mượn nhiều nhất")
    win.geometry("500x300")

    tree = ttk.Treeview(win, columns=("BookName", "TimesBorrowed"), show="headings")
    tree.heading("BookName", text="Tên sách")
    tree.heading("TimesBorrowed", text="Số lần mượn")
    tree.pack(fill="both", expand=True)

    if data:
        for row in data:
            tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("Thông báo", "Chưa có sách nào được mượn.")

    tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)


# Danh sách chưa trả / quá hạn
def show_unreturned_books():
    data = get_unreturned_books()
    win = tk.Toplevel()
    win.title("Danh sách sách chưa trả / quá hạn")
    win.geometry("1400x1200")

    tree = ttk.Treeview(win, columns=("UserID", "UserName", "BookName", "DueDate"), show="headings")
    tree.heading("UserID", text="Mã người dùng")
    tree.heading("UserName", text="Tên người dùng")
    tree.heading("BookName", text="Tên sách")
    tree.heading("DueDate", text="Hạn trả")
    tree.pack(fill="both", expand=True)

    for row in data:
        tree.insert("", "end", values=row)

    tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

# Giao diện chính
class MainMenuApp:
    def __init__(self, root, role):
        self.root = root
        self.root.title("Thư viện - Giao diện chính")
        self.root.geometry("400x500")
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
        tk.Button(self.root, text="Thống kê sách mượn nhiều nhất", command=show_top_borrowed_books).pack(pady=10)
        tk.Button(self.root, text="Sách chưa trả / quá hạn", command=show_unreturned_books).pack(pady=10)
        tk.Button(self.root, text="Đăng xuất", command=self.dang_xuat).pack(pady=10)

    def menu_nguoi_dung(self):
        tk.Label(self.root, text="Giao diện Người dùng", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Trung tâm sách", command=Operations.BookCentre).pack(pady=10)
        tk.Button(self.root, text="Góp ý và đánh giá", command=Operations.Feedback).pack(pady=10)
        tk.Button(self.root, text="Thống kê sách mượn nhiều nhất", command=show_top_borrowed_books).pack(pady=10)
        tk.Button(self.root, text="Đăng xuất", command=self.dang_xuat).pack(pady=10)

    def dang_xuat(self):
        messagebox.showinfo("Đăng xuất", "Cảm ơn bạn đã sử dụng thư viện! Đã đăng xuất.")
        self.root.destroy()

# ========================== ĐĂNG NHẬP ==========================

def open_login_window():
    login_win = tk.Toplevel()
    login_win.title("Đăng nhập")
    login_win.geometry("300x250")

    tk.Label(login_win, text="Vai trò:").pack()
    role_var = tk.StringVar(value="User")
    tk.Radiobutton(login_win, text="Người dùng", variable=role_var, value="User").pack()
    tk.Radiobutton(login_win, text="Quản trị viên", variable=role_var, value="Admin").pack()

    tk.Label(login_win, text="Tài khoản:").pack()
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Mật khẩu:").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def login():
        user = username_entry.get().strip()
        pw = password_entry.get().strip()
        role = role_var.get()

        conn = get_connection()
        cur = conn.cursor()

        if role == "Admin":
            cur.execute("SELECT Passwd FROM AdminRecord WHERE AdminID = %s", (user,))
        else:
            cur.execute("SELECT Passwd FROM UserRecord WHERE UserID = %s", (user,))
        res = cur.fetchone()
        if res and res[0] == pw:
            messagebox.showinfo("Đăng nhập thành công", f"Chào {user}!")
            login_win.destroy()
            root.destroy()
            if role == "Admin":
                Adminmenu()
            else:
                Usermenu()
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập.")

    tk.Button(login_win, text="Đăng nhập", command=login).pack(pady=10)
    tk.Button(login_win, text="Tạo tài khoản người dùng mới", command=lambda: [login_win.destroy(), open_register_window()]).pack()

# ========================== ĐĂNG KÝ ==========================

def open_register_window():
    register_win = tk.Toplevel()
    register_win.title("Tạo tài khoản người dùng")
    register_win.geometry("300x300")

    tk.Label(register_win, text="Mã người dùng:").pack()
    uid_entry = tk.Entry(register_win)
    uid_entry.pack()

    tk.Label(register_win, text="Tên người dùng:").pack()
    name_entry = tk.Entry(register_win)
    name_entry.pack()

    tk.Label(register_win, text="Mật khẩu:").pack()
    pw_entry = tk.Entry(register_win, show="*")
    pw_entry.pack()

    tk.Label(register_win, text="Xác nhận mật khẩu:").pack()
    confirm_entry = tk.Entry(register_win, show="*")
    confirm_entry.pack()

    def register():
        uid = uid_entry.get().strip()
        name = name_entry.get().strip()
        pw = pw_entry.get().strip()
        confirm = confirm_entry.get().strip()

        if not all([uid, name, pw, confirm]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return
        if pw != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT UserID FROM UserRecord WHERE UserID = %s", (uid,))
        if cur.fetchone():
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")
            return

        cur.execute("INSERT INTO UserRecord (UserID, UserName, Passwd, Fullname) VALUES (%s, %s, %s, %s)", (uid, name, pw, name))
        conn.commit()
        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        register_win.destroy()
        open_login_window()

    tk.Button(register_win, text="Đăng ký", command=register).pack(pady=10)

# ========================== MỞ MENU ==========================

def Adminmenu():
    root = tk.Tk()
    MainMenuApp(root, "Admin")
    root.mainloop()

def Usermenu():
    root = tk.Tk()
    MainMenuApp(root, "User")
    root.mainloop()

# ========================== KHỞI ĐỘNG ==========================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hệ thống Quản lý Thư viện")
    root.geometry("300x300")

    tk.Label(root, text="Chào mừng đến với Thư viện", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="Đăng nhập", command=open_login_window).pack(pady=10)

    root.mainloop()
