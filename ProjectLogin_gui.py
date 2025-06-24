import tkinter as tk
from tkinter import messagebox
import pymysql
import MainMenu_gui as MainMenu
import Tables_gui as Tables

class LibraryLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thư viện SÁCH - Đăng nhập")
        self.root.geometry("400x300")

        self.mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="200511",
            database="Library",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.Cursor
        )
        self.mycursor = self.mydb.cursor()

        tk.Label(root, text="~~ T  H  Ư   V  I  Ệ  N   S  Á  C  H ~~", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(root, text="Chọn vai trò để đăng nhập:", font=("Arial", 12)).pack(pady=10)

        tk.Button(root, text="Quản trị viên", width=25, command=self.admin_login_window).pack(pady=5)
        tk.Button(root, text="Người dùng", width=25, command=self.user_login_window).pack(pady=5)
        tk.Button(root, text="Thoát", width=25, command=self.exit_program).pack(pady=10)

    # ---------------- ADMIN ----------------
    def admin_login_window(self):
        self.attempts = 3
        self.admin_win = tk.Toplevel(self.root)
        self.admin_win.title("Đăng nhập Quản trị viên")
        self.admin_win.geometry("300x200")

        tk.Label(self.admin_win, text="Tên đăng nhập:").pack()
        self.admin_id_entry = tk.Entry(self.admin_win)
        self.admin_id_entry.pack()

        tk.Label(self.admin_win, text="Mật khẩu:").pack()
        self.admin_pass_entry = tk.Entry(self.admin_win, show="*")
        self.admin_pass_entry.pack()

        tk.Button(self.admin_win, text="Đăng nhập", command=self.admin_login).pack(pady=10)
        self.attempt_label = tk.Label(self.admin_win, text=f"Số lần thử còn lại: {self.attempts}")
        self.attempt_label.pack()

    def admin_login(self):
        admin_id = self.admin_id_entry.get()
        password = self.admin_pass_entry.get()

        self.mycursor.execute("SELECT Password FROM AdminRecord WHERE AdminID=%s", (admin_id,))
        result = self.mycursor.fetchone()

        if result and result[0] == password:
            messagebox.showinfo("Thành công", f"Xin chào {admin_id}")
            self.admin_win.destroy()
            MainMenu.Adminmenu()
        else:
            self.attempts -= 1
            self.attempt_label.config(text=f"Số lần thử còn lại: {self.attempts}")
            messagebox.showerror("Thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")
            if self.attempts == 0:
                messagebox.showwarning("Cảnh báo", "Bạn đã nhập sai quá 3 lần.")
                self.admin_win.destroy()

    # ---------------- USER ----------------
    def user_login_window(self):
        self.user_win = tk.Toplevel(self.root)
        self.user_win.title("Người dùng")
        self.user_win.geometry("300x150")

        tk.Button(self.user_win, text="Tạo tài khoản mới", command=self.create_account_window).pack(pady=10)
        tk.Button(self.user_win, text="Đăng nhập", command=self.user_login_form).pack(pady=10)

    def create_account_window(self):
        self.create_win = tk.Toplevel(self.user_win)
        self.create_win.title("Tạo tài khoản")
        self.create_win.geometry("300x250")

        tk.Label(self.create_win, text="Mã Người dùng:").pack()
        self.user_id_entry = tk.Entry(self.create_win)
        self.user_id_entry.pack()

        tk.Label(self.create_win, text="Tên Người dùng:").pack()
        self.user_name_entry = tk.Entry(self.create_win)
        self.user_name_entry.pack()

        tk.Label(self.create_win, text="Mật khẩu:").pack()
        self.user_pass_entry = tk.Entry(self.create_win, show="*")
        self.user_pass_entry.pack()

        tk.Label(self.create_win, text="Nhập lại mật khẩu:").pack()
        self.user_confirm_entry = tk.Entry(self.create_win, show="*")
        self.user_confirm_entry.pack()

        tk.Button(self.create_win, text="Tạo", command=self.create_account).pack(pady=10)

    def create_account(self):
        user_id = self.user_id_entry.get()
        user_name = self.user_name_entry.get()
        password = self.user_pass_entry.get()
        confirm = self.user_confirm_entry.get()

        if password != confirm:
            messagebox.showerror("Lỗi", "Hai mật khẩu không trùng khớp.")
            return

        self.mycursor.execute("SELECT UserID FROM UserRecord WHERE UserID=%s", (user_id,))
        if self.mycursor.fetchone():
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")
            return

        self.mycursor.execute("INSERT INTO UserRecord (UserID, UserName, Password, BookID) VALUES (%s, %s, %s, %s)",
                              (user_id, user_name, password, None))
        self.mydb.commit()
        messagebox.showinfo("Thành công", "Tạo tài khoản thành công.")
        self.create_win.destroy()

    def user_login_form(self):
        self.user_attempts = 3
        self.login_win = tk.Toplevel(self.user_win)
        self.login_win.title("Đăng nhập người dùng")
        self.login_win.geometry("300x200")

        tk.Label(self.login_win, text="Mã Người dùng:").pack()
        self.user_id_login = tk.Entry(self.login_win)
        self.user_id_login.pack()

        tk.Label(self.login_win, text="Mật khẩu:").pack()
        self.user_pass_login = tk.Entry(self.login_win, show="*")
        self.user_pass_login.pack()

        tk.Button(self.login_win, text="Đăng nhập", command=self.user_login).pack(pady=10)
        self.user_attempt_label = tk.Label(self.login_win, text=f"Số lần thử còn lại: {self.user_attempts}")
        self.user_attempt_label.pack()

    def user_login(self):
        user_id = self.user_id_login.get()
        password = self.user_pass_login.get()

        self.mycursor.execute("SELECT Password FROM UserRecord WHERE UserID=%s", (user_id,))
        result = self.mycursor.fetchone()

        if result and result[0] == password:
            messagebox.showinfo("Thành công", f"Xin chào {user_id}")
            self.login_win.destroy()
            MainMenu.Usermenu()
        else:
            self.user_attempts -= 1
            self.user_attempt_label.config(text=f"Số lần thử còn lại: {self.user_attempts}")
            messagebox.showerror("Thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")
            if self.user_attempts == 0:
                messagebox.showwarning("Cảnh báo", "Bạn đã nhập sai quá 3 lần.")
                self.login_win.destroy()

    def exit_program(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát không?"):
            self.root.destroy()

# ------------------- MAIN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryLoginApp(root)
    root.mainloop()
