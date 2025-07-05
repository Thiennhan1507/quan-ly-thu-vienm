import tkinter as tk
from tkinter import messagebox, ttk
from db_config import get_connection
from datetime import datetime, timedelta

class BookApp:
    def __init__(self, root):
        self.root = root
        self.mydb = get_connection()
        self.mycursor = self.mydb.cursor()

    # Hiển thị giao diện mượn / trả sách / sách quá hạn
    def show_borrow_return_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        tk.Button(frame, text="Mượn sách", command=self.borrow_book_gui).pack(pady=5)
        tk.Button(frame, text="Trả sách", command=self.return_book_gui).pack(pady=5)
        tk.Button(frame, text="Hiển thị sách quá hạn", command=self.display_overdue_books).pack(pady=5)

    # Hiển thị tất cả sách
    def displayBook(self):
        win = tk.Toplevel()
        win.title("Hiển thị danh sách sách")
        win.geometry("900x400")

        tree = ttk.Treeview(
            win, 
            columns=("BookID", "BookName", "Author", "Publisher", "Quantity", "PublisherYear", "IssuedBy", "UserID"), 
            show="headings"
        )
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""
            SELECT b.BookID, b.BookName, b.Author, b.Publisher, b.quantity, b.PublisherYear,
                   u.UserName, u.UserID
            FROM BookRecord b
            LEFT JOIN transactions t ON b.BookID = t.book_id AND t.status = 'đang mượn'
            LEFT JOIN UserRecord u ON t.user_id = u.UserID
        """)
        records = self.mycursor.fetchall()
        for row in records:
            tree.insert("", "end", values=row)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

    # Thêm sách mới
    def insertBook(self):
        win = tk.Toplevel()
        win.title("Thêm sách mới")
        win.geometry("400x500")

        tk.Label(win, text="Thêm sách", font=("Arial", 14)).pack(pady=10)

        fields = [
            "Mã sách", "Tên sách", "Tác giả", "Nhà xuất bản", "Số lượng", "Năm xuất bản"
        ]
        entries = []
        for label in fields:
            tk.Label(win, text=label).pack()
            entry = tk.Entry(win)
            entry.pack()
            entries.append(entry)

        def add_book():
            values = [e.get().strip() for e in entries]
            if not all(values):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return
            try:
                values[4] = int(values[4])
                values[5] = int(values[5])
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng và Năm xuất bản phải là số.")
                return

            self.mycursor.execute("SELECT * FROM BookRecord WHERE BookID=%s", (values[0],))
            if self.mycursor.fetchone():
                messagebox.showerror("Lỗi", "Mã sách đã tồn tại.")
                return

            self.mycursor.execute(
                "INSERT INTO BookRecord (BookID, BookName, Author, Publisher, quantity, PublisherYear) VALUES (%s, %s, %s, %s, %s, %s)",
                tuple(values)
            )
            self.mydb.commit()
            messagebox.showinfo("Thành công", "Đã thêm sách thành công.")
            if not messagebox.askyesno("Tiếp tục", "Bạn có muốn thêm sách khác không?"):
                win.destroy()

        tk.Button(win, text="Thêm", command=add_book).pack(pady=10)

    # Tìm kiếm sách
    def searchBook(self):
        win = tk.Toplevel()
        win.title("Tìm kiếm sách")
        win.geometry("400x300")

        tk.Label(win, text="Tìm kiếm sách", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Mã sách:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        tk.Label(win, text="Tên sách:").pack()
        book_name_entry = tk.Entry(win)
        book_name_entry.pack()

        tk.Label(win, text="Tác giả:").pack()
        author_entry = tk.Entry(win)
        author_entry.pack()

        def search():
            book_id = book_id_entry.get().strip()
            book_name = book_name_entry.get().strip()
            author = author_entry.get().strip()

            if not any([book_id, book_name, author]):
                messagebox.showerror("Lỗi", "Vui lòng nhập ít nhất một tiêu chí tìm kiếm.")
                return

            query = """
                SELECT b.BookID, b.BookName, b.Author, b.Publisher, b.quantity, b.PublisherYear,
                   u.UserName, u.UserID
                FROM BookRecord b
                LEFT JOIN transactions t ON b.BookID = t.book_id AND t.status = 'đang mượn'
                LEFT JOIN UserRecord u ON t.user_id = u.UserID
                WHERE 1=1
            """
            params = []

            if book_id:
                query += " AND b.BookID = %s"
                params.append(book_id)
            if book_name:
                query += " AND b.BookName LIKE %s"
                params.append(f"%{book_name}%")
            if author:
                query += " AND b.Author LIKE %s"
                params.append(f"%{author}%")

            self.mycursor.execute(query, params)
            records = self.mycursor.fetchall()

            if records:
                result_win = tk.Toplevel()
                result_win.title("Kết quả tìm kiếm")
                result_win.geometry("900x400")

                tree = ttk.Treeview(result_win, columns=(
                    "BookID", "BookName", "Author", "Publisher", "Quantity",
                    "PublisherYear", "BorrowedBy", "BorrowerID"
                ), show="headings")

                headings = [
                    "Mã sách", "Tên sách", "Tác giả", "Nhà xuất bản",
                    "Số lượng", "Năm xuất bản", "Được mượn bởi", "Mã người mượn"
                ]
                for col, text in zip(tree["columns"], headings):
                    tree.heading(col, text=text)

                tree.pack(fill="both", expand=True)

                for row in records:
                    tree.insert("", "end", values=row)

                tk.Button(result_win, text="Đóng", command=result_win.destroy).pack(pady=10)
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy sách.")

        tk.Button(win, text="Tìm kiếm", command=search).pack(pady=10)

    # Xóa sách
    def deleteBook(self):
        win = tk.Toplevel()
        win.title("Xóa sách")
        win.geometry("300x150")

        tk.Label(win, text="Nhập mã sách:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        def delete():
            book_id = book_id_entry.get().strip()
            if not book_id:
                messagebox.showerror("Lỗi", "Vui lòng nhập mã sách.")
                return
            self.mycursor.execute("SELECT * FROM BookRecord WHERE BookID=%s", (book_id,))
            if not self.mycursor.fetchone():
                messagebox.showerror("Lỗi", "Mã sách không tồn tại.")
                return
            self.mycursor.execute("DELETE FROM BookRecord WHERE BookID=%s", (book_id,))
            self.mydb.commit()
            messagebox.showinfo("Thành công", "Đã xóa sách thành công.")
            win.destroy()

        tk.Button(win, text="Xóa", command=delete).pack(pady=10)

    # Cập nhật sách
    def updateBook(self):
        win = tk.Toplevel()
        win.title("Cập nhật sách")
        win.geometry("400x300")

        tk.Label(win, text="Nhập mã sách cần cập nhật:").pack()
        book_id_entry = tk.Entry(win)
        book_id_entry.pack()

        fields = ["Tên sách", "Tác giả", "Nhà xuất bản", "Số lượng", "Năm xuất bản"]
        entries = []
        for label in fields:
            tk.Label(win, text=label).pack()
            e = tk.Entry(win)
            e.pack()
            entries.append(e)

        def update():
            book_id = book_id_entry.get().strip()
            values = [e.get().strip() for e in entries]
            if not all([book_id] + values):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return
            try:
                values[3] = int(values[3])
                values[4] = int(values[4])
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng và Năm xuất bản phải là số.")
                return

            self.mycursor.execute("SELECT * FROM BookRecord WHERE BookID=%s", (book_id,))
            if not self.mycursor.fetchone():
                messagebox.showerror("Lỗi", "Mã sách không tồn tại.")
                return

            self.mycursor.execute("""
                UPDATE BookRecord 
                SET BookName=%s, Author=%s, Publisher=%s, quantity=%s, PublisherYear=%s 
                WHERE BookID=%s
            """, (*values, book_id))
            self.mydb.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật sách.")
            win.destroy()

        tk.Button(win, text="Cập nhật", command=update).pack(pady=10)

    # Mượn sách
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

            self.mycursor.execute("SELECT BookName, quantity FROM BookRecord WHERE BookID=%s", (book_id,))
            result = self.mycursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Sách không tồn tại.")
                return
            book_name, quantity = result
            if quantity <= 0:
                messagebox.showerror("Hết sách", "Sách đã hết.")
                return

            borrow_date = datetime.today().date()
            due_date = borrow_date + timedelta(days=7)

            self.mycursor.execute("""
                INSERT INTO transactions (user_id, book_id, borrow_date, due_date, status)
                VALUES (%s, %s, %s, %s, 'đang mượn')
            """, (user_id, book_id, borrow_date, due_date))
            transaction_id = self.mycursor.lastrowid

            self.mycursor.execute("UPDATE BookRecord SET quantity = quantity - 1 WHERE BookID=%s", (book_id,))
            self.mydb.commit()
            messagebox.showinfo("Thành công", f"Đã mượn sách '{book_name}'.\nHạn trả: {due_date}\nMã giao dịch: {transaction_id}")
            win.destroy()

        tk.Button(win, text="Xác nhận mượn", command=borrow).pack(pady=10)

    # Trả sách
    def return_book_gui(self):
        win = tk.Toplevel()
        win.title("Trả sách")
        win.geometry("300x200")

        tk.Label(win, text="Mã giao dịch:").pack()
        trans_entry = tk.Entry(win)
        trans_entry.pack()

        def return_func():
            trans_id = trans_entry.get().strip()
            self.mycursor.execute("SELECT book_id, due_date, status FROM transactions WHERE transaction_id=%s", (trans_id,))
            result = self.mycursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy giao dịch.")
                return
            book_id, due_date, status = result
            if status == 'đã trả':
                messagebox.showinfo("Thông báo", "Giao dịch đã được trả.")
                return

            return_date = datetime.today().date()
            new_status = 'đã trả' if return_date <= due_date else 'quá hạn'

            self.mycursor.execute("""
                UPDATE transactions SET return_date=%s, status=%s WHERE transaction_id=%s
            """, (return_date, new_status, trans_id))
            self.mycursor.execute("UPDATE BookRecord SET quantity = quantity + 1 WHERE BookID=%s", (book_id,))
            self.mydb.commit()
            messagebox.showinfo("Thành công", f"Trả sách thành công. Trạng thái: {new_status}")
            win.destroy()

        tk.Button(win, text="Xác nhận trả", command=return_func).pack(pady=10)

    # Hiển thị sách quá hạn
    def display_overdue_books(self):
        win = tk.Toplevel()
        win.title("Sách quá hạn")
        win.geometry("700x400")

        tree = ttk.Treeview(win, columns=("BookName", "UserID", "UserName", "BorrowDate", "DueDate", "Status"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""
            SELECT b.BookName, u.UserID, u.UserName, t.borrow_date, t.due_date, t.status
            FROM transactions t
            JOIN BookRecord b ON t.book_id = b.BookID
            JOIN UserRecord u ON t.user_id = u.UserID
            WHERE t.status = 'quá hạn'
        """)
        for row in self.mycursor.fetchall():
            tree.insert("", "end", values=row)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)

    # Hiển thị sách đang mượn
    def display_borrowed_books(self):
        win = tk.Toplevel()
        win.title("Sách đang mượn")
        win.geometry("700x400")

        tree = ttk.Treeview(win, columns=("BookName", "UserID", "UserName", "BorrowDate", "DueDate", "Status"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        self.mycursor.execute("""
            SELECT b.BookName, u.UserID, u.UserName, t.borrow_date, t.due_date, t.status
            FROM transactions t
            JOIN BookRecord b ON t.book_id = b.BookID
            JOIN UserRecord u ON t.user_id = u.UserID
            WHERE t.status = 'đang mượn'
        """)
        for row in self.mycursor.fetchall():
            tree.insert("", "end", values=row)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=10)
