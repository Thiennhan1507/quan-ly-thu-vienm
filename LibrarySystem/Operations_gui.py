import tkinter as tk
from tkinter import messagebox, ttk
import Book_gui as Book  
import User_gui as User   
import Admin_gui as Admin  
from db_config import get_connection

class OperationsApp:
    def __init__(self, root: tk.Tk, menu_type: str):
        self.root = root
        self.root.title(f"Hệ thống Thư viện - {menu_type}")
        self.root.geometry("400x400")
        self.menu_type = menu_type

        # Kết nối DB
        self.mydb = get_connection()
        self.mycursor = self.mydb.cursor()

        # Khởi tạo các app liên quan
        self.book_app = Book.BookApp(self.root)
        self.user_app = User.UserApp()
        self.admin_app = Admin.AdminApp()

        # Điều hướng theo loại menu
        if menu_type == "Quản lý sách":
            self.book_management()
        elif menu_type == "Quản lý người dùng":
            self.user_management()
        elif menu_type == "Quản lý quản trị viên":
            self.admin_management()
        elif menu_type == "Bảng phản hồi":
            self.feedback_table()
        elif menu_type == "Trung tâm sách":
            self.book_centre()
        elif menu_type == "Góp ý và đánh giá":
            self.feedback()

    def book_management(self):
        tk.Label(self.root, text="Quản lý Sách", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Thêm sách", command=self.book_app.insertBook).pack(pady=10)
        tk.Button(self.root, text="Hiển thị sách", command=self.book_app.displayBook).pack(pady=10)
        tk.Button(self.root, text="Tìm kiếm sách", command=self.book_app.searchBook).pack(pady=10)
        tk.Button(self.root, text="Xóa sách", command=self.book_app.deleteBook).pack(pady=10)
        tk.Button(self.root, text="Cập nhật sách", command=self.book_app.updateBook).pack(pady=10)
        tk.Button(self.root, text="Quay lại menu chính", command=self.root.destroy).pack(pady=10)

    def user_management(self):
        tk.Label(self.root, text="Quản lý Người dùng", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Thêm người dùng", command=self.user_app.insertUser).pack(pady=10)
        tk.Button(self.root, text="Hiển thị người dùng", command=self.user_app.displayUser).pack(pady=10)
        tk.Button(self.root, text="Tìm kiếm người dùng", command=self.user_app.searchUser).pack(pady=10)
        tk.Button(self.root, text="Xóa người dùng", command=self.user_app.deleteUser).pack(pady=10)
        tk.Button(self.root, text="Cập nhật người dùng", command=self.user_app.updateUser).pack(pady=10)
        tk.Button(self.root, text="Quay lại menu chính", command=self.root.destroy).pack(pady=10)

    def admin_management(self):
        tk.Label(self.root, text="Quản lý Quản trị viên", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Thêm quản trị viên", command=self.admin_app.them_admin).pack(pady=10)
        tk.Button(self.root, text="Hiển thị quản trị viên", command=self.admin_app.hien_thi_admin).pack(pady=10)
        tk.Button(self.root, text="Tìm kiếm quản trị viên", command=self.admin_app.tim_kiem_admin).pack(pady=10)
        tk.Button(self.root, text="Xóa quản trị viên", command=self.admin_app.xoa_admin).pack(pady=10)
        tk.Button(self.root, text="Cập nhật quản trị viên", command=self.admin_app.cap_nhat_admin).pack(pady=10)


    def feedback_table(self):
        tk.Label(self.root, text="Bảng Góp ý và Đánh giá", font=("Arial", 16)).pack(pady=20)
        
        tree = ttk.Treeview(self.root, columns=("Feedback", "Rating"), show="headings")
        tree.heading("Feedback", text="Nội dung góp ý")
        tree.heading("Rating", text="Đánh giá")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("SELECT * FROM Feedback")
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(self.root, text="Quay lại menu chính", command=self.root.destroy).pack(pady=10)

    def book_centre(self):
        tk.Label(self.root, text="Trung tâm Sách", font=("Arial", 16)).pack(pady=20)
        
        self.book_app.show_borrow_return_ui()
        tk.Button(self.root, text="Danh sách tất cả sách", command=self.book_app.displayBook).pack(pady=10)

        tk.Button(self.root, text="Hiển thị sách đang mượn", command=self.book_app.display_borrowed_books).pack(pady=10)

        tk.Button(self.root, text="Quay lại menu chính", command=self.root.destroy).pack(pady=10)

    def feedback(self):
        feedback_win = tk.Toplevel(self.root)
        feedback_win.title("Góp ý và Đánh giá")
        feedback_win.geometry("400x300")

        tk.Label(feedback_win, text="Đánh giá và Góp ý", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(feedback_win, text="Nội dung góp ý:").pack()
        feedback_entry = tk.Text(feedback_win, height=5, width=30)
        feedback_entry.pack()

        tk.Label(feedback_win, text="Đánh giá (1-10):").pack()
        rating_entry = tk.Entry(feedback_win)
        rating_entry.pack()

        def submit_feedback():
            feedback = feedback_entry.get("1.0", tk.END).strip()
            rating = rating_entry.get()
            if feedback and rating:
                query = "INSERT INTO Feedback (Feedback, Rating) VALUES (%s, %s)"
                self.mycursor.execute(query, (feedback, rating))
                self.mydb.commit()
                messagebox.showinfo("Thành công", "Cảm ơn bạn đã góp ý!")
                feedback_win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")

        tk.Button(feedback_win, text="Gửi góp ý", command=submit_feedback).pack(pady=10)

# ======= Hàm khởi động các màn =======
def BookManagement():
    root = tk.Tk()
    OperationsApp(root, "Quản lý sách")
    root.mainloop()

def UserManagement():
    root = tk.Tk()
    OperationsApp(root, "Quản lý người dùng")
    root.mainloop()

def AdminManagement():
    root = tk.Tk()
    OperationsApp(root, "Quản lý quản trị viên")
    root.mainloop()

def FeedbackTable():
    root = tk.Tk()
    OperationsApp(root, "Bảng phản hồi")
    root.mainloop()

def BookCentre():
    root = tk.Tk()
    OperationsApp(root, "Trung tâm sách")
    root.mainloop()

def Feedback():
    root = tk.Tk()
    OperationsApp(root, "Góp ý và đánh giá")
    root.mainloop()
