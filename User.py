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
        data = ()
        print()
        UserID = input("Nhập mã người dùng: ")
        UserName = input("Nhập họ và tên người dùng: ")
        Password = input("Nhập mật khẩu: ")
        data = (UserID, UserName, Password, None)
        query = "INSERT INTO UserRecord VALUES (%s, %s, %s, %s)"
        mycursor.execute(query, data)
        mydb.commit()
        print("Thêm người dùng thành công!\n")
        ch = input("Bạn có muốn thêm người dùng khác không? [Yes/No]: ")
        if ch.lower() == "no":
            break
    return

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
        Password = input("Nhập mật khẩu mới: ")
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
    database="Library",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.Cursor
)
mycursor = mydb.cursor()
