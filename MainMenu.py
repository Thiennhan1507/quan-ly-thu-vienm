import Operations 
from db_config import get_connection
from getpass import getpass

mydb = get_connection()
mycursor = mydb.cursor()

# ============================ ĐĂNG NHẬP ============================

def login_admin():
    print("\n====== ĐĂNG NHẬP QUẢN TRỊ VIÊN ======\n")
    for attempt in range(3):
        admin_id = input("Nhập Mã Quản trị viên: ").strip()
        password = input("Nhập Mật khẩu: ").strip()

        mycursor.execute("SELECT Password FROM AdminRecord WHERE AdminID = %s", (admin_id,))
        result = mycursor.fetchone()

        if result and result[0] == password:
            print(f"\n>> Xin chào Quản trị viên {admin_id}!")
            Adminmenu()
            return
        else:
            print("Sai thông tin đăng nhập.\n")
    print("Đăng nhập thất bại sau 3 lần thử.")

def login_user():
    print("\n====== ĐĂNG NHẬP NGƯỜI DÙNG ======\n")
    print("1. Tạo tài khoản mới")
    print("2. Đăng nhập")

    ch = input("Lựa chọn: ")
    if ch == "1":
        user_id = input("Mã người dùng: ").strip()
        name = input("Tên người dùng: ").strip()
        passwd = input("Mật khẩu: ").strip()
        confirm = input("Xác nhận mật khẩu: ").strip()

        if passwd != confirm:
            print("Mật khẩu không trùng khớp.")
            return

        mycursor.execute("SELECT UserID FROM UserRecord WHERE UserID=%s", (user_id,))
        if mycursor.fetchone():
            print("Mã người dùng đã tồn tại.")
            return

        mycursor.execute("INSERT INTO UserRecord (UserID, UserName, Passwd, Fullname, BookID) VALUES (%s, %s, %s, %s, %s)",
                         (user_id, name, passwd, name, None))
        mydb.commit()
        print("Tạo tài khoản thành công. Hãy đăng nhập lại.")
        login_user()

    elif ch == "2":
        for attempt in range(3):
            user_id = input("Mã người dùng: ").strip()
            password = input("Mật khẩu: ").strip()

            mycursor.execute("SELECT Passwd FROM UserRecord WHERE UserID=%s", (user_id,))
            result = mycursor.fetchone()

            if result and result[0] == password:
                print(f"\n>> Xin chào {user_id}!")
                Usermenu()
                return
            else:
                print("Thông tin đăng nhập không đúng.\n")
        print("Đăng nhập thất bại sau 3 lần thử.")
    else:
        print("Lựa chọn không hợp lệ.")


# ============================ MENU CHÍNH ============================

def Adminmenu():
    while True:
        print("\nMENU QUẢN TRỊ VIÊN")
        print("1. Quản lý Sách")
        print("2. Quản lý Người dùng")
        print("3. Quản lý Quản trị viên")
        print("4. Bảng Góp ý và Đánh giá")
        print("5. Đăng xuất")
        ch = input(">> Chọn: ")
        if ch == "1":
            Operations.BookManagement()
        elif ch == "2":
            Operations.UserManagement()
        elif ch == "3":
            Operations.AdminManagement()
        elif ch == "4":
            Operations.FeedbackTable()
        elif ch == "5":
            print("Đã đăng xuất.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

def Usermenu():
    while True:
        print("\nMENU NGƯỜI DÙNG")
        print("1. Trung tâm Sách")
        print("2. Góp ý & Đánh giá")
        print("3. Đăng xuất")
        ch = input(">> Chọn: ")
        if ch == "1":
            Operations.BookCentre()
        elif ch == "2":
            Operations.Feedback()
        elif ch == "3":
            print("Đã đăng xuất.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

# ============================ KHỞI ĐỘNG ============================

if __name__ == "__main__":
    print("\n====== HỆ THỐNG QUẢN LÝ THƯ VIỆN ======\n")
    print("1. Đăng nhập Quản trị viên")
    print("2. Đăng nhập Người dùng")
    print("0. Thoát")

    ch = input(">> Chọn: ")
    if ch == "1":
        login_admin()
    elif ch == "2":
        login_user()
    elif ch == "0":
        print("Tạm biệt!")
    else:
        print("Lựa chọn không hợp lệ.")