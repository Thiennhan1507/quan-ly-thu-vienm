import pymysql
import Tables

#----------------------------------------------------------------------------------------
# Quản trị viên thao tác với Sách
def displayBook():
    print()
    print("Danh sách Hồ sơ Sách: \n")
    mycursor.execute("""SELECT BookRecord.BookID,BookRecord.BookName,BookRecord.Author,BookRecord.Publisher,UserRecord.UserName,UserRecord.UserID
                        FROM BookRecord
                        LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID""")
    records = mycursor.fetchall()
    row_no = 0
    for rows in records:
        row_no += 1
        print("******************************", "Hàng số", row_no, "******************************")
        print("\t             Mã sách: ", rows[0])
        print("\t            Tên sách: ", rows[1])
        print("\t               Tác giả: ", rows[2])
        print("\t              Nhà xuất bản: ", rows[3])
        print("\t             Được mượn bởi: ", rows[4])
        print("\t             Mã người mượn: ", rows[5])
        print()
    input("Nhấn Enter để quay lại menu")

#----------------------------------------------------------------------------------------
def insertBook():
    while True:
        print()
        BookID = input("Nhập Mã sách: ")
        BookName = input("Nhập Tên sách: ")
        Author = input("Nhập Tên tác giả: ")
        Publisher = input("Nhập Tên nhà xuất bản: ")
        data = (BookID, BookName, Author, Publisher)
        query = "INSERT INTO BookRecord VALUES (%s, %s, %s, %s)"
        mycursor.execute(query, data)
        mydb.commit()
        print()
        ch = input("Bạn có muốn thêm sách khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break

#----------------------------------------------------------------------------------------
def deleteBook():
    while True:
        print()
        BookID = input("Nhập Mã sách cần xóa: ")
        mycursor.execute("DELETE from BookRecord where BookID = {0} ".format("'" + BookID + "'"))
        mydb.commit()
        ch = input("Bạn có muốn xóa sách khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break

#----------------------------------------------------------------------------------------
def searchBook():
    while True:
        print()
        Search = input("Nhập Mã sách cần tìm: ")
        mycursor.execute("""SELECT BookRecord.BookID,BookRecord.BookName,BookRecord.Author,BookRecord.Publisher,UserRecord.UserName,UserRecord.UserID
                            FROM BookRecord
                            LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID
                            WHERE BookRecord.BookID={0}""".format("'" + Search + "'"))
        records = mycursor.fetchall()
        if records:
            for rows in records:
                print("******************************", "Kết quả tìm kiếm", "******************************")
                print("\t             Mã sách: ", rows[0])
                print("\t            Tên sách: ", rows[1])
                print("\t               Tác giả: ", rows[2])
                print("\t              Nhà xuất bản: ", rows[3])
                print("\t             Được mượn bởi: ", rows[4])
                print("\t             Mã người mượn: ", rows[5])
                print()
        else:
            print("Không tìm thấy sách.")
        ch = input("Bạn có muốn tìm thêm sách khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break

#----------------------------------------------------------------------------------------
def updateBook():
    while True:
        print()
        BookID = input("Nhập Mã sách cần cập nhật: ")
        BookName = input("Nhập Tên sách mới: ")
        Author = input("Nhập Tên tác giả mới: ")
        Publisher = input("Nhập Nhà xuất bản mới: ")
        query = "UPDATE BookRecord SET Bookname = %s, Author = %s, Publisher = %s WHERE BookID = %s"
        data = (BookName, Author, Publisher, BookID)
        mycursor.execute(query, data)
        mydb.commit()
        print("Cập nhật thành công!")
        ch = input("Bạn có muốn cập nhật sách khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break

#----------------------------------------------------------------------------------------
# Người dùng thao tác với Sách
def BookList():
    print()
    print("Danh sách Sách: \n")
    mycursor.execute("SELECT * FROM BookRecord")
    records = mycursor.fetchall()
    row_no = 0
    for rows in records:
        row_no += 1
        print("******************************", "Hàng số", row_no, "******************************")
        print("\t             Mã sách: ", rows[0])
        print("\t            Tên sách: ", rows[1])
        print("\t               Tác giả: ", rows[2])
        print("\t              Nhà xuất bản: ", rows[3])
        print()
    input("Nhấn Enter để quay lại menu")

#----------------------------------------------------------------------------------------
def IssueBook():
    check = input("Nhập Mã người dùng của bạn: ")
    mycursor.execute("SELECT BookID FROM UserRecord WHERE UserID={0}".format("'" + check + "'"))
    checking = mycursor.fetchone()
    if checking == (None,):
        print()
        print("Danh sách sách hiện có:\n")
        mycursor.execute("""SELECT BookRecord.BookID,BookRecord.BookName, BookRecord.Author,BookRecord.Publisher,UserRecord.UserName,UserRecord.UserID
                            FROM BookRecord
                            LEFT JOIN UserRecord ON BookRecord.BookID=UserRecord.BookID""")
        records = mycursor.fetchall()
        row_no = 0
        for rows in records:
            if rows[5] == None:
                row_no += 1
                print("******************************", "Hàng số", row_no, "******************************")
                print("\t             Mã sách: ", rows[0])
                print("\t            Tên sách: ", rows[1])
                print("\t               Tác giả: ", rows[2])
                print("\t              Nhà xuất bản: ", rows[3])
                print()
        if row_no == 0:
            print("Rất tiếc, hiện tại không còn sách trống trong thư viện.")
            print("Vui lòng đợi cho đến khi có người trả sách bạn muốn.")
            input("Nhấn Enter để quay lại menu")
            return
        UserID = input("Nhập Mã người dùng của bạn: ")
        Issue = input("Nhập Mã sách bạn muốn mượn: ")
        query = "UPDATE UserRecord SET BookID=%s WHERE UserID = %s"
        data = (Issue, UserID)
        mycursor.execute(query, data)
        mydb.commit()
        print("Mượn sách thành công!")
        input("Nhấn Enter để quay lại menu")
    else:
        print("Bạn đã mượn sách rồi, vui lòng trả sách trước khi mượn tiếp.")
        input("Nhấn Enter để quay lại menu")

#----------------------------------------------------------------------------------------
def ShowIssuedBook():
    print()
    UserID = input("Nhập Mã người dùng của bạn: ")
    mycursor.execute("""SELECT UserID, UserName, UserRecord.BookID, BookName
                        FROM Library.UserRecord INNER JOIN Library.BookRecord
                        ON BookRecord.BookID=UserRecord.BookID
                        WHERE UserID={0}""".format("'" + UserID + "'"))
    records = mycursor.fetchall()
    if records:
        for rows in records:
            print("******************************", "Sách đã mượn", "******************************")
            print("\t             Mã người dùng: ", rows[0])
            print("\t            Tên người dùng: ", rows[1])
            print("\t             Mã sách: ", rows[2])
            print("\t            Tên sách: ", rows[3])
            print()
        input("Nhấn Enter để quay lại menu")
    else:
        print("Bạn chưa mượn sách nào.")
        input("Nhấn Enter để quay lại menu")

#----------------------------------------------------------------------------------------
def returnBook():
    print()
    UserID = input("Nhập Mã người dùng của bạn: ")
    Rec = input("Nhập Mã sách bạn muốn trả: ")
    query = """UPDATE UserRecord SET BookID = %s WHERE UserID= %s AND BookID=%s"""
    data = (None, UserID, Rec)
    mycursor.execute(query, data)
    mydb.commit()
    print("Trả sách thành công!")
    input("Nhấn Enter để quay lại menu")

#----------------------------------------------------------------------------------------
mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="200511",
    database="Library",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.Cursor
)
mycursor = mydb.cursor()

