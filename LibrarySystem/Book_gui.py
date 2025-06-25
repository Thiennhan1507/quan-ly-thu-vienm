import tkinter as tk
from tkinter import messagebox, ttk
from db_config import get_connection
from datetime import datetime, timedelta

conn = get_connection()
cursor = conn.cursor()

class BookApp:
    def __init__(self, root):
        self.root = root
        self.mydb = get_connection()
        self.mycursor = self.mydb.cursor()

    def show_borrow_return_ui(self):
        # Tạo giao diện chính để đặt các nút mượn và trả sách
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        # Nút mượn sách → mở form mượn sách
        tk.Button(frame, text="Mượn sách", command=self.borrow_book_gui).pack(pady=5)
        tk.Button(frame, text="Trả sách", command=self.return_book_gui).pack(pady=5)

        # Nút hiển thị sách quá hạn 
        tk.Button(frame, text="Hiển thị sách quá hạn", command=self.display_overdue_books).pack(pady=5)


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
            book_id = book_id_entry.get().strip()
            if not book_id:
                messagebox.showerror("Lỗi", "Vui lòng nhập mã sách.")
                return

            # Kiểm tra sách có tồn tại không
            self.mycursor.execute("SELECT BookName FROM BookRecord WHERE BookID = %s", (book_id,))
            result = self.mycursor.fetchone()
            if not result:
                messagebox.showwarning("Không tìm thấy", f"Sách với mã {book_id} không tồn tại.")
                return

            book_name = result[0]
            # Xác nhận xóa
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sách '{book_name}'?")
            if not confirm:
                return

            # Thực hiện xóa
            self.mycursor.execute("DELETE FROM BookRecord WHERE BookID=%s", (book_id,))
            self.mydb.commit()
            messagebox.showinfo("Thành công", f"Đã xóa sách: {book_name}")
            win.destroy()

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
            book_id = book_id_entry.get().strip()
            book_name = book_name_entry.get().strip()
            author = author_entry.get().strip()
            publisher = publisher_entry.get().strip()

            if not all([book_id, book_name, author, publisher]):
                    messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
                    return

            # Kiểm tra sách tồn tại
            self.mycursor.execute("SELECT BookName FROM BookRecord WHERE BookID = %s", (book_id,))
            result = self.mycursor.fetchone()
            if not result:
                messagebox.showwarning("Không tìm thấy", f"Sách với mã {book_id} không tồn tại.")
                return

            self.mycursor.execute("""
                UPDATE BookRecord 
                SET BookName=%s, Author=%s, Publisher=%s 
                WHERE BookID=%s
                """, (book_name, author, publisher, book_id))
            self.mydb.commit()

            messagebox.showinfo("Thành công", f"Đã cập nhật sách có mã: {book_id}")
            win.destroy()

        tk.Button(win, text="Cập nhật", command=update_book).pack(pady=10)

    # mượn sách 
    def borrow_book_gui(self):
        win = tk.Toplevel()
        win.title("Mượn sách")
        win.geometry("300x250")

        tk.Label(win, text="Mã người dùng:").pack()
        user_entry = tk.Entry(win)
        user_entry.pack()

        tk.Label(win, text="Mã sách:").pack()
        book_entry = tk.Entry(win)
        book_entry.pack()

        def borrow():
            user_id = user_entry.get().strip()
            book_id = book_entry.get().strip()

            cursor.execute("SELECT BookName, quantity FROM BookRecord WHERE BookID = %s", (book_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Sách không tồn tại.")
                return
            book_name, quantity = result
            if quantity <= 0:
                messagebox.showwarning("Hết sách", "Sách đã hết.")
                return

            borrow_date = datetime.today().date()
            due_date = borrow_date + timedelta(days=7)

            cursor.execute("""
                INSERT INTO transactions (user_id, book_id, borrow_date, due_date, status)
                VALUES (%s, %s, %s, %s, 'borrowed')
                """, (user_id, book_id, borrow_date, due_date))

            cursor.execute("UPDATE BookRecord SET quantity = quantity - 1 WHERE BookID = %s", (book_id,))
            conn.commit()

            messagebox.showinfo("Thành công", f"Đã mượn sách: {book_name}\nHạn trả: {due_date}")
            win.destroy()

        tk.Button(win, text="Xác nhận mượn", command=borrow).pack(pady=10)

    # trả sách 
    def return_book_gui(self):
        win = tk.Toplevel()
        win.title("Trả sách")
        win.geometry("300x200")

        tk.Label(win, text="Mã giao dịch:").pack()
        trans_entry = tk.Entry(win)
        trans_entry.pack()

        def return_func():
            trans_id = trans_entry.get().strip()
            cursor.execute("SELECT book_id, due_date, status FROM transactions WHERE transaction_id = %s", (trans_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy giao dịch.")
                return
            book_id, due_date, status = result
            if status == 'returned':
                messagebox.showinfo("Thông báo", "Giao dịch đã được trả.")
                return

            return_date = datetime.today().date()
            new_status = 'returned' if return_date <= due_date else 'overdue'

            cursor.execute("""
                UPDATE transactions SET return_date=%s, status=%s
                WHERE transaction_id=%s
                """, (return_date, new_status, trans_id))

            cursor.execute("UPDATE BookRecord SET quantity = quantity + 1 WHERE BookID = %s", (book_id,))
            conn.commit()

            messagebox.showinfo("Thành công", f"Trả sách thành công. Trạng thái: {new_status}")
            win.destroy()

        tk.Button(win, text="Xác nhận trả", command=return_func).pack(pady=10)

    # hiển thị sách quá hạn 
    def display_overdue_books(self):
        win = tk.Toplevel()
        win.title("Sách quá hạn")
        win.geometry("700x400")

        tree = ttk.Treeview(win, columns=("BookName", "UserID", "UserName", "BorrowDate", "DueDate", "Status"), show="headings")
        tree.heading("BookName", text="Tên sách")
        tree.heading("UserID", text="Mã người mượn")
        tree.heading("UserName", text="Họ tên người mượn")
        tree.heading("BorrowDate", text="Ngày mượn")
        tree.heading("DueDate", text="Hạn trả")
        tree.heading("Status", text="Trạng thái")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""
            SELECT b.BookName, u.UserID, u.UserName, t.borrow_date, t.due_date, t.status
            FROM transactions t
            JOIN BookRecord b ON t.book_id = b.BookID
            JOIN UserRecord u ON t.user_id = u.UserID
            WHERE t.status = 'overdue'
            """)
        records = self.mycursor.fetchall()

        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

    def display_borrowed_books(self):
        win = tk.Toplevel()
        win.title("Danh sách sách đang được mượn")
        win.geometry("700x400")

        tree = ttk.Treeview(win, columns=("BookName", "UserID", "UserName", "BorrowDate", "DueDate", "Status"), show="headings")
        tree.heading("BookName", text="Tên sách")
        tree.heading("UserID", text="Mã người mượn")
        tree.heading("UserName", text="Họ tên người mượn")
        tree.heading("BorrowDate", text="Ngày mượn")
        tree.heading("DueDate", text="Hạn trả")
        tree.heading("Status", text="Trạng thái")
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""
            SELECT b.BookName, u.UserID, u.UserName, t.borrow_date, t.due_date, t.status
            FROM transactions t
            JOIN BookRecord b ON t.book_id = b.BookID
            JOIN UserRecord u ON t.user_id = u.UserID
            WHERE t.status = 'borrowed'
            """)
        records = self.mycursor.fetchall()

        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)
