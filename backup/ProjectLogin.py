import sys
import MainMenu
import Tables
import pymysql
from db_config import get_connection 

#---------------------------------------------------------------------------------------------------------
def login_to_admin():  # Đăng nhập Admin
    print("\n")
    print("|                 ~~  T  H  Ư   V  I  Ệ  N     S  Á  C  H   ~~                    |")
    print()
    print("                ĐĂNG NHẬP TÀI KHOẢN QUẢN TRỊ VIÊN\n")
    print("CẢNH BÁO: Bạn chỉ có 3 lần thử đăng nhập")
    for attempts in range(0, 3):
        AdminID = input("\t  Nhập Mã Quản trị viên: ")
        password = input("\t  Nhập Mật khẩu: ")
        print()
        mycursor.execute("SELECT Password FROM AdminRecord WHERE AdminID = %s", (AdminID,))
        result = mycursor.fetchone()
        if result:
            temp, = result
            if temp == password:
                print(f"\n\t\t    CHÀO MỪNG {AdminID} ĐẾN VỚI THƯ VIỆN SÁCH\n")
                MainMenu.Adminmenu()
                break
            else:
                print("\t MẬT KHẨU HOẶC TÊN ĐĂNG NHẬP KHÔNG ĐÚNG! THỬ LẠI.")
                print(f"\t Đã hết lần thử thứ {attempts + 1}\n")
        else:
            print("\t KHÔNG TÌM THẤY TÊN ĐĂNG NHẬP! THỬ LẠI.")
            print(f"\t Đã hết lần thử thứ {attempts + 1}\n")
    else:
        print("\t Vui lòng thử lại sau.")
        print("\t Hệ thống tạm dừng.\n")
        print("*---------------------------------------------------------------------------------* \n")

#---------------------------------------------------------------------------------------------------------
def login_to_user():  # Đăng nhập người dùng
    print("\n")
    print("|                 ~~  T  H  Ư   V  I  Ệ  N     S  Á  C  H   ~~                    |")
    print()
    print("1. TẠO TÀI KHOẢN")
    print("2. ĐĂNG NHẬP TÀI KHOẢN")
    ch = int(input("Nhập lựa chọn --> "))
    if ch == 1:
        while True:
            UserId = input("Nhập Mã người dùng: ")
            UserName = input("Nhập Tên người dùng: ")
            Password = input("Nhập Mật khẩu muốn đặt: ")
            ConfirmPassword = input("Nhập lại Mật khẩu: ")

            if Password != ConfirmPassword:
                print("Hai mật khẩu không trùng khớp. Vui lòng nhập lại.\n")
                continue  # quay lại nhập lại

            # Kiểm tra trùng mã người dùng
            mycursor.execute("SELECT UserId FROM UserRecord WHERE UserId=%s", (UserId,))
            if mycursor.fetchone():
                print("Tài khoản với mã này đã tồn tại. Vui lòng dùng mã khác.\n")
                continue

            # Lưu tài khoản vào CSDL
            query = "INSERT INTO UserRecord (UserID, UserName, Password, BookID) VALUES (%s, %s, %s, %s)"
            mycursor.execute(query, (UserId, UserName, Password, None))
            mydb.commit()
            print("Tài khoản đã được tạo thành công.\n")
            break

        login_to_user()

    elif ch == 2:
        print("CẢNH BÁO: Bạn chỉ có 3 lần thử đăng nhập")
        for attempts in range(0, 3):
            UserID = input("\t  Nhập Mã người dùng: ")
            password = input("\t  Nhập Mật khẩu: ")
            print()
            mycursor.execute("SELECT Password FROM UserRecord WHERE UserID={0}".format("'" + UserID + "'"))
            result = mycursor.fetchone()
            if result:
                temp, = result
                if temp == password:
                    print(f"\n\t\t    CHÀO MỪNG {UserID} ĐẾN VỚI THƯ VIỆN SÁCH\n")
                    MainMenu.Usermenu()
                    break
                else:
                    print("\t MẬT KHẨU HOẶC TÊN ĐĂNG NHẬP KHÔNG ĐÚNG! THỬ LẠI.")
                    print(f"\t Đã hết lần thử thứ {attempts + 1}\n")
            else:
                print("\t KHÔNG TÌM THẤY TÊN ĐĂNG NHẬP! THỬ LẠI.")
                print(f"\t Đã hết lần thử thứ {attempts + 1}\n")
        else:
            print("\t Vui lòng thử lại sau.")
            print("\t Hệ thống tạm dừng.\n")
            print("*---------------------------------------------------------------------------------* \n")
    else:
        print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
        login_to_user()

#---------------------------------------------------------------------------------------------------------
def menu():
    print("\n\n")
    print("|*************************************************************************************|")
    print("|                 ~~  T  H  Ư   V  I  Ệ  N     S  Á  C  H   ~~                    |")
    print("|*************************************************************************************|")
    print("\n")
    print("                 =================== MENU CHÍNH ===================\n")
    print(" 1. Đăng nhập với vai trò QUẢN TRỊ VIÊN")
    print(" 2. Đăng nhập với vai trò NGƯỜI DÙNG")
    print(" 3. THOÁT\n")

    while True:
        ch = input("Chọn [1/2/3]: ")
        print()
        if ch == "1":
            login_to_admin()
            break
        elif ch == "2":
            login_to_user()
            break
        elif ch == "3":
            cancel_request = input(" BẠN CÓ MUỐN THOÁT KHÔNG? [yes/no]: ")
            if cancel_request.lower() == "yes":
                sys.exit()
            break
        else:
            print("LỆNH KHÔNG HỢP LỆ.")
            print("VUI LÒNG THỬ LẠI.\n")

#---------------------------------------------------------------------------------------------------------
mydb = get_connection()
mycursor = mydb.cursor()


menu()
