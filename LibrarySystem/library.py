from datetime import datetime, timedelta
from db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

# Kiểm tra số lượng sách còn để mượn
def check_book_availability(book_id):
    """
    Kiểm tra sách còn số lượng để mượn không.
    Trả về True nếu còn, False nếu hết.
    """
    cursor.execute("SELECT quantity FROM BookRecord WHERE BookID = %s", (book_id,))
    result = cursor.fetchone()
    return result and result[0] > 0

# Thêm giao dịch mượn sách vào transactions, giảm số lượng sách
def borrow_book(user_id, book_id):
    """
    Hàm xử lý mượn sách:
    - Kiểm tra sách có tồn tại và còn số lượng không.
    - Thêm giao dịch mượn vào bảng `transactions`.
    - Giảm số lượng sách trong bảng BookRecord.
    """
    # Kiểm tra sách có tồn tại
    cursor.execute("SELECT title FROM BookRecord WHERE BookID = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("Sách không tồn tại.")
        return

    # Kiểm tra sách còn không
    if not check_book_availability(book_id):
        print("Sách đã hết.")
        return

    borrow_date = datetime.today().date()
    due_date = borrow_date + timedelta(days=7)

    # Thêm giao dịch mượn vào bảng transactions
    cursor.execute("""
        INSERT INTO transactions (user_id, book_id, borrow_date, due_date, status)
        VALUES (%s, %s, %s, %s, 'borrowed')
    """, (user_id, book_id, borrow_date, due_date))

    # Giảm số lượng sách trong BookRecord
    cursor.execute("UPDATE BookRecord SET quantity = quantity - 1 WHERE BookID = %s", (book_id,))
    conn.commit()
    print(f"Mượn sách thành công: {book[0]} (Hạn trả: {due_date})")

# Trả sách, cập nhật trạng thái và tăng số lượng sách
def return_book(transaction_id):
    """
    Hàm xử lý trả sách:
    - Kiểm tra giao dịch tồn tại chưa.
    - Nếu đã trả rồi → không xử lý lại.
    - Nếu chưa, cập nhật ngày trả và trạng thái 'returned' hoặc 'overdue'.
    - Tăng lại số lượng sách trong BookRecord.
    """
    return_date = datetime.today().date()

    # Lấy thông tin giao dịch (từ bảng transactions)
    cursor.execute("SELECT book_id, due_date, status FROM transactions WHERE transaction_id = %s", (transaction_id,))
    result = cursor.fetchone()

    if not result:
        print("Giao dịch không tồn tại.")
        return

    book_id, due_date, current_status = result

    # Kiểm tra nếu sách đã được trả
    if current_status == 'returned':
        print("Giao dịch này đã được trả trước đó.")
        return

    # Xác định trạng thái mới: returned hoặc overdue
    status = 'returned' if return_date <= due_date else 'overdue'

    # Cập nhật trạng thái giao dịch và ngày trả
    cursor.execute("""
        UPDATE transactions
        SET return_date = %s, status = %s
        WHERE transaction_id = %s
    """, (return_date, status, transaction_id))

    # Cập nhật lại số lượng sách trong bảng BookRecord
    cursor.execute("UPDATE BookRecord SET quantity = quantity + 1 WHERE BookID = %s", (book_id,))
    conn.commit()

    print(f"Trả sách thành công. Trạng thái: {status}")

# Thống kê top sách được mượn nhiều nhất
def get_top_borrowed_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.BookName, COUNT(*) AS TimesBorrowed
        FROM transactions t
        JOIN BookRecord b ON t.book_id = b.BookID
        GROUP BY t.book_id
        ORDER BY TimesBorrowed DESC
        LIMIT 10;
    """)

    results = cursor.fetchall()
    return results


# Lấy danh sách sách đang mượn hoặc quá hạn chưa trả
def get_unreturned_books():
    cursor.execute("""
        SELECT u.UserID, u.UserName, b.BookName, t.due_date
        FROM transactions t
        JOIN UserRecord u ON t.user_id = u.UserID
        JOIN BookRecord b ON t.book_id = b.BookID
        WHERE t.status IN ('borrowed', 'overdue') AND t.return_date IS NULL
    """)
    return cursor.fetchall()

def main_menu():
    """
    Giao diện dòng lệnh chính cho chức năng Mượn/Trả sách.
    """
    while True:
        print("\n===== MENU QUẢN LÝ MƯỢN/TRẢ SÁCH =====")
        print("1. Mượn sách")
        print("2. Trả sách")
        print("3. Thống kê sách mượn nhiều nhất")
        print("0. Thoát")
        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            try:
                user_id = input("Nhập ID người dùng: ")
                book_id = input("Nhập ID sách: ")
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

