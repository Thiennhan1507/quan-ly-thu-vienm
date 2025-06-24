import pymysql
from datetime import datetime, timedelta

conn = pymysql.connect(
            host="localhost",
            user="root",
            passwd="200511",
            database="Library",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor
        )
cursor = conn.cursor()


def check_book_availability(book_id):
    cursor.execute("SELECT quantity FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    return result and result[0] > 0


def borrow_book(user_id, book_id):
    cursor.execute("SELECT title FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("Sách không tồn tại.")
        return

    if not check_book_availability(book_id):
        print("Sách đã hết.")
        return

    borrow_date = datetime.today().date()
    due_date = borrow_date + timedelta(days=7)

    cursor.execute("""
        INSERT INTO transactions (user_id, book_id, borrow_date, due_date, status)
        VALUES (%s, %s, %s, %s, 'borrowed')
    """, (user_id, book_id, borrow_date, due_date))

    cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    print(f"Mượn sách thành công: {book[0]} (Hạn trả: {due_date})")


def return_book(transaction_id):
    return_date = datetime.today().date()

    cursor.execute("SELECT book_id, due_date FROM transactions WHERE transaction_id = %s", (transaction_id,))
    result = cursor.fetchone()

    if not result:
        print("Giao dịch không tồn tại.")
        return

    book_id, due_date = result
    status = 'returned' if return_date <= due_date else 'overdue'

    cursor.execute("""
        UPDATE transactions
        SET return_date = %s, status = %s
        WHERE transaction_id = %s
    """, (return_date, status, transaction_id))

    cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    print(f"Trả sách thành công. Trạng thái: {status}")


def get_top_borrowed_books(limit=5):
    cursor.execute("""
        SELECT b.title, COUNT(*) AS times_borrowed
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        GROUP BY b.book_id
        ORDER BY times_borrowed DESC
        LIMIT %s
    """, (limit,))

    results = cursor.fetchall()
    if not results:
        print("Không có dữ liệu mượn sách.")
        return

    print("Sách được mượn nhiều nhất:")
    for title, count in results:
        print(f"- {title} ({count} lần)")


def main_menu():
    while True:
        print("\n===== MENU QUẢN LÝ MƯỢN/TRẢ SÁCH =====")
        print("1. Mượn sách")
        print("2. Trả sách")
        print("3. Thống kê sách mượn nhiều nhất")
        print("0. Thoát")
        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            try:
                user_id = int(input("Nhập ID người dùng: "))
                book_id = int(input("Nhập ID sách: "))
                borrow_book(user_id, book_id)
            except:
                print("Dữ liệu nhập không hợp lệ.")
        elif choice == '2':
            try:
                transaction_id = int(input("Nhập ID giao dịch: "))
                return_book(transaction_id)
            except:
                print("Dữ liệu nhập không hợp lệ.")
        elif choice == '3':
            get_top_borrowed_books()
        elif choice == '0':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == "__main__":
    main_menu()
