import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
import Tables_gui as Tables

class AdminApp:
    def __init__(self):
        self.mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="200511",
            database="Library",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor
        )
        self.mycursor = self.mydb.cursor()

    def hien_thi_admin(self):
        win = tk.Toplevel()
        win.title("Hiển thị thông tin Quản trị viên")
        win.geometry("400x400")

        tree = ttk.Treeview(win, columns=("AdminID", "Password"), show="headings")
        tree.heading("AdminID", text="Tên đăng nhập")
        tree.heading("Password", text="Mật khẩu")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("SELECT * FROM AdminRecord")
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=(row[0], row[1]))

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

    def them_admin(self):
        win = tk.Toplevel()
        win.title("Thêm Quản trị viên")
        win.geometry("300x200")

        tk.Label(win, text="Thêm quản trị viên", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Tên đăng nhập:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        tk.Label(win, text="Mật khẩu:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        def add_admin():
            admin_id = admin_id_entry.get()
            password = password_entry.get()
            if admin_id and password:
                query = "INSERT INTO AdminRecord VALUES (%s, %s)"
                self.mycursor.execute(query, (admin_id, password))
                self.mydb.commit()
                messagebox.showinfo("Thành công", "Thêm quản trị viên thành công.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn thêm quản trị viên khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")

        tk.Button(win, text="Thêm", command=add_admin).pack(pady=10)

    def xoa_admin(self):
        win = tk.Toplevel()
        win.title("Xóa Quản trị viên")
        win.geometry("300x150")

        tk.Label(win, text="Xóa quản trị viên", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Tên đăng nhập:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        def delete_admin():
            admin_id = admin_id_entry.get()
            if admin_id:
                self.mycursor.execute("DELETE FROM AdminRecord WHERE AdminID=%s", (admin_id,))
                self.mydb.commit()
                messagebox.showinfo("Thành công", "Xóa quản trị viên thành công.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn xóa quản trị viên khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập Tên đăng nhập.")

        tk.Button(win, text="Xóa", command=delete_admin).pack(pady=10)

    def tim_kiem_admin(self):
        win = tk.Toplevel()
        win.title("Tìm kiếm Quản trị viên")
        win.geometry("300x200")

        tk.Label(win, text="Tìm kiếm quản trị viên", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Tên đăng nhập:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        def search_admin():
            admin_id = admin_id_entry.get()
            if admin_id:
                self.mycursor.execute("SELECT * FROM AdminRecord WHERE AdminID=%s", (admin_id,))
                records = self.mycursor.fetchall()
                if records:
                    result_win = tk.Toplevel()
                    result_win.title("Kết quả tìm kiếm")
                    result_win.geometry("300x150")
                    for row in records:
                        tk.Label(result_win, text=f"Tên đăng nhập: {row[0]}").pack()
                        tk.Label(result_win, text=f"Mật khẩu: {row[1]}").pack()
                    tk.Button(result_win, text="Đóng", command=result_win.destroy).pack(pady=10)
                else:
                    messagebox.showinfo("Kết quả", "Không tìm thấy tài khoản.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn tìm thêm tài khoản khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập Tên đăng nhập.")

        tk.Button(win, text="Tìm kiếm", command=search_admin).pack(pady=10)

    def cap_nhat_admin(self):
        win = tk.Toplevel()
        win.title("Cập nhật Quản trị viên")
        win.geometry("300x200")

        tk.Label(win, text="Cập nhật quản trị viên", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Tên đăng nhập:").pack()
        admin_id_entry = tk.Entry(win)
        admin_id_entry.pack()

        tk.Label(win, text="Mật khẩu mới:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        def update_admin():
            admin_id = admin_id_entry.get()
            password = password_entry.get()
            if admin_id and password:
                query = "UPDATE AdminRecord SET Password=%s WHERE AdminID=%s"
                self.mycursor.execute(query, (password, admin_id))
                self.mydb.commit()
                messagebox.showinfo("Thành công", "Cập nhật mật khẩu thành công.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn cập nhật tài khoản khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")

        tk.Button(win, text="Cập nhật", command=update_admin).pack(pady=10)
