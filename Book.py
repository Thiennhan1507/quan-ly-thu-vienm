from db_config import get_connection
from datetime import datetime, timedelta

mydb = get_connection()
mycursor = mydb.cursor()

# Hiển thị danh sách sách
def displayBook():
    print("\nDanh sách Sách: \n")
    mycursor.execute("SELECT * FROM BookRecord")
    records = mycursor.fetchall()
    for i, row in enumerate(records, 1):
        print(f"--- Sách số {i} ---")
        print(f"Mã sách: {row[0]}")
        print(f"Tên sách: {row[1]}")
        print(f"Tác giả: {row[2]}")
        print(f"Nhà xuất bản: {row[3]}")
        print(f"Số lượng còn lại: {row[4]}")
        print()
    input("Nhấn Enter để quay lại menu")

# Thêm sách
def insertBook():
    while True:
        print()
        BookID = input("Nhập Mã sách: ")
        BookName = input("Nhập Tên sách: ")
        Author = input("Nhập Tên tác giả: ")
        Publisher = input("Nhập Nhà xuất bản: ")
        quantity = int(input("Nhập số lượng: "))

        query = "INSERT INTO BookRecord (BookID, BookName, Author, Publisher, quantity) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(query, (BookID, BookName, Author, Publisher, quantity))
        mydb.commit()

        print("Thêm sách thành công!")
        ch = input("Bạn có muốn thêm sách khác không? [Yes/No]: ")
        if ch.lower() != "yes":
            break

# Xóa sách
def deleteBook():
    while True:
        BookID = input("Nhập Mã sách cần xóa: ")
        mycursor.execute("DELETE FROM BookRecord WHERE BookID = %s", (BookID,))
        mydb.commit()
        print("Đã xóa sách.")
        ch = input("Bạn có muốn xóa sách khác không? [Yes/No]: ")
        if ch.lower() != "yes":
            break

# Tìm sách
def searchBook():
    while True:
        BookID = input("Nhập Mã sách cần tìm: ")
        mycursor.execute("SELECT * FROM BookRecord WHERE BookID = %s", (BookID,))
        row = mycursor.fetchone()
        if row:
            print(f"\nMã sách: {row[0]}")
            print(f"Tên sách: {row[1]}")
            print(f"Tác giả: {row[2]}")
            print(f"Nhà xuất bản: {row[3]}")
            print(f"Số lượng còn lại: {row[4]}")
        else:
            print("Không tìm thấy sách.")
        ch = input("Bạn có muốn tìm sách khác không? [Yes/No]: ")
        if ch.lower() != "yes":
            break

# Cập nhật sách
def updateBook():
    while True:
        BookID = input("Nhập Mã sách cần cập nhật: ")
        BookName = input("Tên sách mới: ")
        Author = input("Tác giả mới: ")
        Publisher = input("Nhà xuất bản mới: ")
        quantity = int(input("Số lượng mới: "))

        query = """UPDATE BookRecord 
                   SET BookName = %s, Author = %s, Publisher = %s, quantity = %s
                   WHERE BookID = %s"""
        mycursor.execute(query, (BookName, Author, Publisher, quantity, BookID))
        mydb.commit()
        print("Cập nhật thành công!")

        ch = input("Bạn có muốn cập nhật sách khác không? [Yes/No]: ")
        if ch.lower() != "yes":
            break

# Mượn sách
def IssueBook():
    user_id = input("Nhập Mã người dùng của bạn: ")
    book_id = input("Nhập Mã sách bạn muốn mượn: ")

    mycursor.execute("SELECT BookName, quantity FROM BookRecord WHERE BookID = %s", (book_id,))
    result = mycursor.fetchone()
    if not result:
        print("Sách không tồn tại.")
        return
    book_name, quantity = result
    if quantity <= 0:
        print("Sách đã hết.")
        return

    borrow_date = datetime.today().date()
    due_date = borrow_date + timedelta(days=7)

    mycursor.execute("""
        INSERT INTO transactions (user_id, book_id, borrow_date, due_date, status)
        VALUES (%s, %s, %s, %s, 'borrowed')
        """, (user_id, book_id, borrow_date, due_date))

    mycursor.execute("UPDATE BookRecord SET quantity = quantity - 1 WHERE BookID = %s", (book_id,))
    mydb.commit()

    print(f"Đã mượn sách: {book_name}\nHạn trả: {due_date}")

# Trả sách
def returnBook():
    trans_id = input("Nhập Mã giao dịch mượn sách: ")

    mycursor.execute("SELECT book_id, due_date, status FROM transactions WHERE transaction_id = %s", (trans_id,))
    result = mycursor.fetchone()
    if not result:
        print("Không tìm thấy giao dịch.")
        return
    book_id, due_date, status = result
    if status == 'returned':
        print("Sách đã được trả.")
        return

    return_date = datetime.today().date()
    new_status = 'returned' if return_date <= due_date else 'overdue'

    mycursor.execute("""
        UPDATE transactions SET return_date=%s, status=%s
        WHERE transaction_id=%s
        """, (return_date, new_status, trans_id))

    mycursor.execute("UPDATE BookRecord SET quantity = quantity + 1 WHERE BookID = %s", (book_id,))
    mydb.commit()

    print(f"Trả sách thành công. Trạng thái: {new_status}")

# Hiển thị sách đã mượn
def ShowIssuedBook():
    user_id = input("Nhập Mã người dùng của bạn: ")
    mycursor.execute("""
        SELECT t.transaction_id, b.BookName, t.borrow_date, t.due_date, t.status
        FROM transactions t
        JOIN BookRecord b ON t.book_id = b.BookID
        WHERE t.user_id = %s AND t.status IN ('borrowed', 'overdue')
    """, (user_id,))
    records = mycursor.fetchall()
    if records:
        print(f"\nDanh sách sách đang mượn của {user_id}:\n")
        for row in records:
            print(f"Mã giao dịch: {row[0]}")
            print(f"Tên sách: {row[1]}")
            print(f"Ngày mượn: {row[2]}")
            print(f"Hạn trả: {row[3]}")
            print(f"Trạng thái: {row[4]}")
            print()
    else:
        print("Không có sách đang mượn.")

# Hiển thị sách quá hạn
def ShowOverdueBooks():
    print("\nDanh sách sách quá hạn:\n")
    mycursor.execute("""
        SELECT b.BookName, u.UserID, u.UserName, t.borrow_date, t.due_date, t.status
        FROM transactions t
        JOIN BookRecord b ON t.book_id = b.BookID
        JOIN UserRecord u ON t.user_id = u.UserID
        WHERE t.status = 'overdue'
    """)
    records = mycursor.fetchall()
    for row in records:
        print(f"Tên sách: {row[0]}")
        print(f"Mã người mượn: {row[1]}")
        print(f"Tên người mượn: {row[2]}")
        print(f"Ngày mượn: {row[3]}")
        print(f"Hạn trả: {row[4]}")
        print(f"Trạng thái: {row[5]}")
        print()
    input("Nhấn Enter để quay lại menu...")
