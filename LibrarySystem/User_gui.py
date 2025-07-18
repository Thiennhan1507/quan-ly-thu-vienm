import tkinter as tk
from tkinter import messagebox, ttk
from db_config import get_connection

class UserApp:
    def __init__(self):
        self.mydb = get_connection()
        self.mycursor = self.mydb.cursor()

    def displayUser(self):
        win = tk.Toplevel()
        win.title("Hiển thị danh sách người dùng")
        win.geometry("500x400")

        tree = ttk.Treeview(win, columns=("UserID", "UserName", "Passwd"), show="headings")
        for col, name in zip(tree["columns"], ["Mã người dùng", "Tên người dùng", "Mật khẩu"]):
            tree.heading(col, text=name)
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("SELECT UserID, UserName, Passwd FROM UserRecord")
        for row in self.mycursor.fetchall():
            tree.insert("", "end", values=row)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

    def insertUser(self):
        win = tk.Toplevel()
        win.title("Thêm người dùng")
        win.geometry("300x300")

        tk.Label(win, text="Thêm người dùng", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Mã người dùng:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        tk.Label(win, text="Tên người dùng:").pack()
        user_name_entry = tk.Entry(win)
        user_name_entry.pack()

        tk.Label(win, text="Mật khẩu:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        tk.Label(win, text="Nhập lại mật khẩu:").pack()
        confirm_entry = tk.Entry(win, show="*")
        confirm_entry.pack()

        def add_user():
            user_id = user_id_entry.get().strip()
            user_name = user_name_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()

            if not all([user_id, user_name, password, confirm]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return

            if password != confirm:
                messagebox.showerror("Lỗi", "Hai mật khẩu không trùng khớp.")
                return

            # Kiểm tra UserID tồn tại
            self.mycursor.execute("SELECT UserID FROM UserRecord WHERE UserID = %s", (user_id,))
            if self.mycursor.fetchone():
                messagebox.showerror("Lỗi", "Mã người dùng đã tồn tại.")
                return
            
            self.mycursor.execute(
                "INSERT INTO UserRecord (UserID, UserName, Passwd, Fullname) VALUES (%s, %s, %s, %s)",
                (user_id, user_name, password, user_name)  # user_name được dùng cho cả 2 trường
    )
            self.mydb.commit()
            messagebox.showinfo("Thành công", "Đã thêm người dùng thành công.")
            if not messagebox.askyesno("Tiếp tục", "Bạn có muốn thêm người dùng khác không?"):
                win.destroy()

        tk.Button(win, text="Thêm", command=add_user).pack(pady=10)

    def deleteUser(self):
        win = tk.Toplevel()
        win.title("Xóa người dùng")
        win.geometry("300x150")

        tk.Label(win, text="Xóa người dùng", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Mã người dùng:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        def delete_user():
            user_id = user_id_entry.get().strip()
            if not user_id:
                messagebox.showerror("Lỗi", "Vui lòng nhập mã người dùng.")
                return

            self.mycursor.execute("SELECT * FROM UserRecord WHERE UserID = %s", (user_id,))
            if not self.mycursor.fetchone():
                messagebox.showerror("Lỗi", "Người dùng không tồn tại.")
                return

            self.mycursor.execute("DELETE FROM UserRecord WHERE UserID=%s", (user_id,))
            self.mydb.commit()
            messagebox.showinfo("Thành công", "Đã xóa người dùng thành công.")
            if not messagebox.askyesno("Tiếp tục", "Bạn có muốn xóa người dùng khác không?"):
                win.destroy()

        tk.Button(win, text="Xóa", command=delete_user).pack(pady=10)

    def searchUser(self):
        win = tk.Toplevel()
        win.title("Tìm kiếm người dùng")
        win.geometry("300x200")

        tk.Label(win, text="Tìm kiếm người dùng", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Mã người dùng:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        def search_user():
            user_id = user_id_entry.get().strip()
            if not user_id:
                messagebox.showerror("Lỗi", "Vui lòng nhập mã người dùng.")
                return

            self.mycursor.execute("SELECT UserID, UserName, Passwd FROM UserRecord WHERE UserID = %s", (user_id,))
            record = self.mycursor.fetchone()
            if record:
                result_win = tk.Toplevel()
                result_win.title("Kết quả tìm kiếm")
                result_win.geometry("400x150")
                tk.Label(result_win, text=f"Mã người dùng: {record[0]}").pack()
                tk.Label(result_win, text=f"Tên người dùng: {record[1]}").pack()
                tk.Label(result_win, text=f"Mật khẩu: {record[2]}").pack()
                tk.Button(result_win, text="Đóng", command=result_win.destroy).pack(pady=10)
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy người dùng.")
            if not messagebox.askyesno("Tiếp tục", "Bạn có muốn tìm người dùng khác không?"):
                win.destroy()

        tk.Button(win, text="Tìm kiếm", command=search_user).pack(pady=10)

    def updateUser(self):
        win = tk.Toplevel()
        win.title("Cập nhật thông tin người dùng")
        win.geometry("300x280")

        tk.Label(win, text="Cập nhật người dùng", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Mã người dùng:").pack()
        user_id_entry = tk.Entry(win)
        user_id_entry.pack()

        tk.Label(win, text="Tên người dùng mới:").pack()
        user_name_entry = tk.Entry(win)
        user_name_entry.pack()

        tk.Label(win, text="Mật khẩu mới:").pack()
        password_entry = tk.Entry(win, show="*")
        password_entry.pack()

        tk.Label(win, text="Nhập lại mật khẩu mới:").pack()
        confirm_entry = tk.Entry(win, show="*")
        confirm_entry.pack()

        def update_user():
            user_id = user_id_entry.get().strip()
            user_name = user_name_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()

            if not all([user_id, user_name, password, confirm]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return
            if password != confirm:
                messagebox.showerror("Lỗi", "Hai mật khẩu không trùng khớp.")
                return

            self.mycursor.execute("SELECT * FROM UserRecord WHERE UserID = %s", (user_id,))
            if not self.mycursor.fetchone():
                messagebox.showerror("Lỗi", "Người dùng không tồn tại.")
                return

            self.mycursor.execute("UPDATE UserRecord SET UserName = %s, Passwd = %s WHERE UserID = %s",
                                  (user_name, password, user_id))
            self.mydb.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin người dùng.")
            if not messagebox.askyesno("Tiếp tục", "Bạn có muốn cập nhật người dùng khác không?"):
                win.destroy()

        tk.Button(win, text="Cập nhật", command=update_user).pack(pady=10)
