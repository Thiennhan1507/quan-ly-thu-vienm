import pymysql
from db_config import get_connection

# Kết nối CSDL
mydb = get_connection()
mycursor = mydb.cursor()

#--------------------------------------------------------------------------------------------------------------------------------      
# hiển thị danh sách người dùng 
def displayUser():
    print()
    print("Danh sách người dùng: \n")
    mycursor.execute("SELECT UserID, UserName, Passwd FROM UserRecord")
    records = mycursor.fetchall()
    row_no = 0
    for rows in records:
        row_no += 1
        print("******************************", "Người dùng số", row_no, "******************************")
        print("\t   Mã người dùng: ", rows[0])
        print("\t     Họ và tên: ", rows[1])
        print("\t       Mật khẩu: ", rows[2])
        print()
    input("Nhấn phím bất kỳ để quay lại menu...")

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
            continue

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
        query = "INSERT INTO UserRecord (UserID, UserName, Passwd) VALUES (%s, %s, %s)"
        try:
            mycursor.execute(query, (UserID, UserName, Password))
            mydb.commit()
            print("Thêm người dùng thành công!\n")
        except pymysql.MySQLError as err:
            print(f"Lỗi CSDL: {err}")
            continue

        ch = input("Bạn có muốn thêm người dùng khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break

#--------------------------------------------------------------------------------------------------------------------------------             
# xóa người dùng 
def deleteUser():
    while True:
        print()
        UserID = input("Nhập mã người dùng cần xóa: ").strip()
        if not UserID:
            print("Mã người dùng không được để trống.")
            continue

        mycursor.execute("SELECT * FROM UserRecord WHERE UserID = %s", (UserID,))
        if not mycursor.fetchone():
            print("Người dùng không tồn tại.")
        else:
            mycursor.execute("DELETE FROM UserRecord WHERE UserID = %s", (UserID,))
            mydb.commit()
            print("Đã xóa người dùng thành công!")

        ch = input("Bạn có muốn xóa người dùng khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break

#--------------------------------------------------------------------------------------------------------------------------------  
# tìm kiếm người dùng        
def searchUser():
    while True:
        print()
        UserID = input("Nhập mã người dùng cần tìm: ").strip()
        if not UserID:
            print("Vui lòng nhập mã người dùng.")
            continue

        mycursor.execute("SELECT UserID, UserName, Passwd FROM UserRecord WHERE UserID = %s", (UserID,))
        record = mycursor.fetchone()
        if record:
            print("****************************** Kết quả tìm kiếm ******************************")
            print("\t   Mã người dùng: ", record[0])
            print("\t     Họ và tên: ", record[1])
            print("\t       Mật khẩu: ", record[2])
            print()
        else:
            print("Không tìm thấy người dùng.")

        ch = input("Bạn có muốn tìm thêm người dùng khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break

#--------------------------------------------------------------------------------------------------------------------------------    
# cập nhật người dùng  
def updateUser():
    while True:
        print()
        UserID = input("Nhập mã người dùng cần cập nhật: ").strip()
        if not UserID:
            print("Mã người dùng không được để trống.")
            continue

        mycursor.execute("SELECT * FROM UserRecord WHERE UserID = %s", (UserID,))
        if not mycursor.fetchone():
            print("Người dùng không tồn tại.")
            continue

        UserName = input("Nhập tên người dùng mới: ").strip()
        while True:
            Password = input("Nhập mật khẩu mới: ").strip()
            ConfirmPassword = input("Nhập lại mật khẩu mới: ").strip()
            if Password != ConfirmPassword:
                print("Hai mật khẩu không trùng khớp. Vui lòng nhập lại.\n")
            else:
                break

        query = "UPDATE UserRecord SET UserName = %s, Passwd = %s WHERE UserID = %s"
        mycursor.execute(query, (UserName, Password, UserID))
        mydb.commit()
        print("Cập nhật thành công!")

        ch = input("Bạn có muốn cập nhật người dùng khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break
    return 
