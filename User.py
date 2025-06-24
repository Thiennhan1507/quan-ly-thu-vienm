import pymysql
import Tables

#--------------------------------------------------------------------------------------------------------------------------------      
# hiển thị danh sách người dùng 
def displayUser():
    print()
    print("Danh sách người dùng: \n")
    mycursor.execute("""SELECT UserRecord.UserID,UserRecord.UserName,UserRecord.Password,BookRecord.BookName,BookRecord.BookID
                        FROM UserRecord
                        LEFT JOIN BookRecord ON UserRecord.BookID=BookRecord.BookID""")
    records = mycursor.fetchall()
    row_no = 0
    for rows in records:
        row_no += 1
        print("******************************", "Người dùng số", row_no, "******************************")
        print("\t             Mã người dùng: ", rows[0])
        print("\t               Họ và tên: ", rows[1])
        print("\t                 Mật khẩu: ", rows[2])
        print("\t        Sách đang mượn: ", rows[3])
        print("\t              Mã sách: ", rows[4])
        print()
    input("Nhấn phím bất kỳ để quay lại menu...")
    return

#--------------------------------------------------------------------------------------------------------------------------------         
# thêm tài khoản người dùng     
def insertUser():
    while True:
        print()
        UserID = input("Nhập mã người dùng (ví dụ: FnB1234): ").strip()
        UserName = input("Nhập họ và tên người dùng: ").strip()

        # Kiểm tra trùng mã người dùng
        mycursor.execute("SELECT UserID FROM UserRecord WHERE UserID = %s", (UserID,))
        if mycursor.fetchone():
            print("Mã người dùng đã tồn tại. Vui lòng thử mã khác.\n")
            continue  # Quay lại vòng lặp để nhập lại

        # Nhập và xác nhận mật khẩu
        while True:
            Password = input("Nhập mật khẩu: ").strip()
            ConfirmPassword = input("Nhập lại mật khẩu: ").strip()
            if Password != ConfirmPassword:
                print("Hai mật khẩu không trùng khớp. Vui lòng nhập lại.\n")
            elif not Password:
                print("Mật khẩu không được để trống.\n")
            else:
                break

        # Thêm vào CSDL
        query = "INSERT INTO UserRecord (UserID, UserName, Password, BookID) VALUES (%s, %s, %s, %s)"
        data = (UserID, UserName, Password, None)
        try:
            mycursor.execute(query, data)
            mydb.commit()
            print("Thêm người dùng thành công!\n")
        except pymysql.connect.Error as err:
            print(f"Lỗi CSDL: {err}")
            continue

        # Hỏi tiếp tục
        ch = input("Bạn có muốn thêm người dùng khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break

#--------------------------------------------------------------------------------------------------------------------------------             
# xóa người dùng 
def deleteUser():
    while True:
        print()
        UserID = input("Nhập mã người dùng cần xóa: ")
        mycursor.execute("DELETE FROM UserRecord WHERE UserID = %s", (UserID,))
        mydb.commit()
        print("Xóa người dùng thành công!")
        ch = input("Bạn có muốn xóa người dùng khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break
    return

#--------------------------------------------------------------------------------------------------------------------------------  
# tìm kiếm người dùng        
def searchUser():
    while True:
        print()
        Search = input("Nhập mã người dùng cần tìm: ")
        mycursor.execute("""SELECT UserID, UserName, Password , BookName, UserRecord.BookID
                            FROM Library.UserRecord 
                            LEFT JOIN Library.BookRecord ON BookRecord.BookID = UserRecord.BookID
                            WHERE UserRecord.UserID = %s""", (Search,))
        records = mycursor.fetchall()
        if records:
            for rows in records:
                print("******************************", "Kết quả tìm kiếm", "******************************")
                print("\t             Mã người dùng: ", rows[0])
                print("\t               Họ và tên: ", rows[1])
                print("\t                 Mật khẩu: ", rows[2])
                print("\t        Sách đang mượn: ", rows[3])
                print("\t              Mã sách: ", rows[4])
                print()
        else:
            print("Không tìm thấy người dùng.")

        ch = input("Bạn có muốn tìm thêm người dùng khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break
    return

#--------------------------------------------------------------------------------------------------------------------------------    
# cập nhật người dùng  
def updateUser():
    while True:
        print()
        UserID = input("Nhập mã người dùng cần cập nhật: ")
        UserName = input("Nhập tên người dùng mới: ")
        while True:
            Password = input("Nhập mật khẩu mới: ")
            ConfirmPassword = input("Nhập lại mật khẩu mới: ")
            if Password != ConfirmPassword:
                print("Hai mật khẩu không trùng khớp. Vui lòng nhập lại.\n")
            else:
                break # mật khẩu hợp lệ

        query = "UPDATE UserRecord SET Username = %s, Password = %s WHERE UserID = %s"
        data = (UserName, Password, UserID)
        mycursor.execute(query, data)
        mydb.commit()
        print("Cập nhật thành công!")
        
        ch = input("Bạn có muốn cập nhật người dùng khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break
    return    
#--------------------------------------------------------------------------------------------------------------------------------     
mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="200511",
    database="Library"
)
mycursor = mydb.cursor()
