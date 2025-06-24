import Operations

def Adminmenu():
    while True:
        print("\t\t\t Menu Quản trị viên \n")
        print("==============================================================")
        print("1. Quản lý Sách")
        print("2. Quản lý Người dùng")
        print("3. Quản lý Quản trị viên")
        print("4. Bảng Góp ý và Đánh giá của Người dùng")
        print("5. Đăng xuất")
        print("===============================================================")
        choice = int(input("Nhập lựa chọn từ 1 đến 5 -------> : "))
        if choice == 1:
            Operations.BookManagement()
        elif choice == 2:
            Operations.UserManagement()
        elif choice == 3:
            Operations.AdminManagement()
        elif choice == 4:
            Operations.FeedbackTable()
        elif choice == 5:
            print("Cảm ơn bạn đã ghé thăm Thư viện của chúng tôi :))")
            print("Đã đăng xuất khỏi hệ thống")
            break
        else:
            print("Lựa chọn không hợp lệ......Vui lòng nhập lại lựa chọn của bạn")
            continue

def Usermenu():
    while True:
        print("\t\t\t Menu Người dùng \n")
        print("==============================================================")
        print("1. Trung tâm Sách")
        print("2. Góp ý và Đánh giá")
        print("3. Đăng xuất")
        print("===============================================================")
        choice = int(input("Nhập lựa chọn từ 1 đến 3 -------> : "))
        if choice == 1:
            Operations.BookCentre()
        elif choice == 2:
            Operations.Feedback()
        elif choice == 3:
            print("Cảm ơn bạn đã ghé thăm Thư viện của chúng tôi :))")
            print("Đã đăng xuất khỏi hệ thống")
            break
        else:
            print("Lựa chọn không hợp lệ......Vui lòng nhập lại lựa chọn của bạn")
            continue

if __name__ == "__main__":
    print("===== Chào mừng đến với Hệ thống Quản lý Thư viện =====")
    print("1. Đăng nhập Quản trị viên")
    print("2. Đăng nhập Người dùng")
    role = input("Nhập lựa chọn của bạn (1 cho Quản trị viên, 2 cho Người dùng): ")

    if role == "1":
        Adminmenu()
    elif role == "2":
        Usermenu()
    else:
        print("Lựa chọn không hợp lệ. Đang thoát...")
