import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
import Tables_gui as Tables
from db_config import get_connection
class BookApp:
    def __init__(self):
        self.mydb = get_connection()
        self.mycursor = self.mydb.cursor()

    def displayBook(self):
        win = tk.Toplevel()
        win.title("Hiển thị danh sách sách")
        win.geometry("600x400")

        tree = ttk.Treeview(win, columns=("BookID", "BookName", "Author", "Publisher", "IssuedBy", "UserID"), show="headings")
        tree.heading("BookID", text="Mã sách")
        tree.heading("BookName", text="Tên sách")
        tree.heading("Author", text="Tác giả")
        tree.heading("Publisher", text="Nhà xuất bản")
        tree.heading("IssuedBy", text="Được mượn bởi")
        tree.heading("UserID", text="Mã người mượn")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher, 
                                UserRecord.UserName, UserRecord.UserID
                                FROM BookRecord LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID""")
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

    def insertBook(self):
        win = tk.Toplevel()
        win.title("Thêm sách mới")
        win.geometry("300x300")

        tk.Label(win, text="Thêm sách", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="Mã sách:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        tk.Label(win, text="Tên sách:").pack()
        book_name_entry = tk.Entry(win)
        book_name_entry.pack()

        tk.Label(win, text="Tác giả:").pack()
        author_entry = tk.Entry(win)
        author_entry.pack()

        tk.Label(win, text="Nhà xuất bản:").pack()
        publisher_entry = tk.Entry(win)
        publisher_entry.pack()

        def add_book():
            book_id = book_id_entry.get()
            book_name = book_name_entry.get()
            author = author_entry.get()
            publisher = publisher_entry.get()
            if all([book_id, book_name, author, publisher]):
                query = "INSERT INTO BookRecord VALUES (%s, %s, %s, %s)"
                self.mycursor.execute(query, (book_id, book_name, author, publisher))
                self.mydb.commit()
                messagebox.showinfo("Thành công", "Đã thêm sách thành công.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn thêm sách khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")

        tk.Button(win, text="Thêm", command=add_book).pack(pady=10)

    def deleteBook(self):
        win = tk.Toplevel()
        win.title("Xóa sách")
        win.geometry("300x150")

        tk.Label(win, text="Xóa sách", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="Nhập mã sách:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        def delete_book():
            book_id = book_id_entry.get()
            if book_id:
                self.mycursor.execute("DELETE FROM BookRecord WHERE BookID=%s", (book_id,))
                self.mydb.commit()
                messagebox.showinfo("Thành công", "Đã xóa sách.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn xóa sách khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập mã sách.")

        tk.Button(win, text="Xóa", command=delete_book).pack(pady=10)

    def searchBook(self):
        win = tk.Toplevel()
        win.title("Tìm kiếm sách")
        win.geometry("300x200")

        tk.Label(win, text="Tìm kiếm sách", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="Nhập mã sách:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        def search_book():
            book_id = book_id_entry.get()
            if book_id:
                self.mycursor.execute("""SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, BookRecord.Publisher,
                                        UserRecord.UserName, UserRecord.UserID
                                        FROM BookRecord LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID
                                        WHERE BookRecord.BookID=%s""", (book_id,))
                records = self.mycursor.fetchall()
                if records:
                    result_win = tk.Toplevel()
                    result_win.title("Kết quả tìm kiếm")
                    result_win.geometry("400x200")
                    for row in records:
                        tk.Label(result_win, text=f"Mã sách: {row[0]}").pack()
                        tk.Label(result_win, text=f"Tên sách: {row[1]}").pack()
                        tk.Label(result_win, text=f"Tác giả: {row[2]}").pack()
                        tk.Label(result_win, text=f"Nhà xuất bản: {row[3]}").pack()
                        tk.Label(result_win, text=f"Được mượn bởi: {row[4]}").pack()
                        tk.Label(result_win, text=f"Mã người mượn: {row[5]}").pack()
                    tk.Button(result_win, text="Đóng", command=result_win.destroy).pack(pady=10)
                else:
                    messagebox.showinfo("Thông báo", "Không tìm thấy sách.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn tìm sách khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập mã sách.")

        tk.Button(win, text="Tìm kiếm", command=search_book).pack(pady=10)

    def updateBook(self):
        win = tk.Toplevel()
        win.title("Cập nhật sách")
        win.geometry("300x300")

        tk.Label(win, text="Cập nhật sách", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, text="Mã sách:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        tk.Label(win, text="Tên sách mới:").pack()
        book_name_entry = tk.Entry(win)
        book_name_entry.pack()

        tk.Label(win, text="Tác giả mới:").pack()
        author_entry = tk.Entry(win)
        author_entry.pack()

        tk.Label(win, text="Nhà xuất bản mới:").pack()
        publisher_entry = tk.Entry(win)
        publisher_entry.pack()

        def update_book():
            book_id = book_id_entry.get()
            book_name = book_name_entry.get()
            author = author_entry.get()
            publisher = publisher_entry.get()
            if all([book_id, book_name, author, publisher]):
                query = "UPDATE BookRecord SET BookName=%s, Author=%s, Publisher=%s WHERE BookID=%s"
                self.mycursor.execute(query, (book_name, author, publisher, book_id))
                self.mydb.commit()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin sách.")
                if not messagebox.askyesno("Tiếp tục", "Bạn có muốn cập nhật sách khác không?"):
                    win.destroy()
            else:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")

        tk.Button(win, text="Cập nhật", command=update_book).pack(pady=10)
