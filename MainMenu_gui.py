import tkinter as tk
from tkinter import messagebox, ttk
import Operations_gui as Operations
from Book_gui import BookApp
from library import get_top_borrowed_books
from library import get_unreturned_books 
# Hàm thống kê sách mượn nhiều nhất
def show_top_borrowed_books():
    data = get_top_borrowed_books()

    win = tk.Toplevel()
    win.title("Thống kê sách mượn nhiều nhất")
    win.geometry("500x300")

    tree = ttk.Treeview(win, columns=("BookName", "TimesBorrowed"), show="headings")
    tree.heading("BookName", text="Tên sách")
    tree.heading("TimesBorrowed", text="Số lần mượn")
    tree.pack(fill="both", expand=True)

    for row in data:
        tree.insert("", "end", values=row)

    tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

# danh sách chưa trả hoặc quá hạn 
def show_unreturned_books():
    data = get_unreturned_books()

    win = tk.Toplevel()
    win.title("Danh sách sách chưa trả / quá hạn")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("UserID", "UserName", "BookName", "DueDate"), show="headings")
    tree.heading("UserID", text="Mã người dùng")
    tree.heading("UserName", text="Tên người dùng")
    tree.heading("BookName", text="Tên sách")
    tree.heading("DueDate", text="Hạn trả")

    tree.pack(fill="both", expand=True)

    for row in data:
        tree.insert("", "end", values=row)

    tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

# Lớp giao diện chính
class MainMenuApp:
    def __init__(self, root, role):
        self.root = root
        self.root.title("Thư viện - Giao diện chính")
        self.root.geometry("400x500")  # Tăng chiều cao để chứa thêm nút thống kê
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


# Gọi hàm tạo menu tương ứng
def Adminmenu():
    root = tk.Tk()
    app = MainMenuApp(root, "Admin")
    root.mainloop()


def Usermenu():
    root = tk.Tk()
    app = MainMenuApp(root, "User")
    root.mainloop()


# Tùy chọn muốn chạy mặc định là admin hay user
if __name__ == "__main__":
    Adminmenu()  # Hoặc Usermenu() nếu muốn mở mặc định giao diện người dùng 
