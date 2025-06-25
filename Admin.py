from db_config import get_connection

mydb = get_connection()
mycursor = mydb.cursor()
#---------------------------------------------------------------------------------------------------------
# hiển thị danh sách quản trị viên 
def displayAdmin():
    print("\nDanh sách Quản trị viên: \n")
    mycursor.execute("SELECT * FROM AdminRecord")
    records = mycursor.fetchall()

    if not records:
        print("Hiện chưa có quản trị viên nào trong hệ thống.")
    else:
        for i, row in enumerate(records, 1):
            print("****************************** Hàng số", i, "******************************")
            print("\t Mã Quản trị viên:", row[0])
            print("\t Mật khẩu:", row[1])
            print()
    input("Nhấn Enter để tiếp tục...")
    return

#---------------------------------------------------------------------------------------------------------
# thêm quản trị viên
def insertAdmin():
    while True:
        print()
        AdminID = input("Nhập Mã Quản trị viên mới: ").strip()

        # Kiểm tra trùng mã
        mycursor.execute("SELECT AdminID FROM AdminRecord WHERE AdminID = %s", (AdminID,))
        if mycursor.fetchone():
            print("Mã Quản trị viên đã tồn tại. Vui lòng dùng mã khác.\n")
            continue

        # Nhập và xác nhận mật khẩu
        while True:
            Password = input("Nhập Mật khẩu: ").strip()
            Confirm = input("Nhập lại Mật khẩu: ").strip()
            if Password != Confirm:
                print("Hai mật khẩu không khớp. Vui lòng nhập lại.\n")
            elif not Password:
                print("Mật khẩu không được để trống.\n")
            else:
                break

        mycursor.execute("INSERT INTO AdminRecord (AdminID, Password) VALUES (%s, %s)", (AdminID, Password))
        mydb.commit()
        print("Thêm Quản trị viên thành công.\n")

        ch = input("Bạn có muốn thêm Quản trị viên khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break
    return

#---------------------------------------------------------------------------------------------------------
# xóa quản trị viên 
def deleteAdmin():
    while True:
        print()
        AdminID = input("Nhập Mã Quản trị viên cần xóa: ").strip()
        mycursor.execute("SELECT * FROM AdminRecord WHERE AdminID = %s", (AdminID,))
        if not mycursor.fetchone():
            print("Không tìm thấy mã Quản trị viên này.\n")
            continue

        mycursor.execute("DELETE FROM AdminRecord WHERE AdminID = %s", (AdminID,))
        mydb.commit()
        print("Xóa Quản trị viên thành công.\n")

        ch = input("Bạn có muốn xóa Quản trị viên khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break
    return

#---------------------------------------------------------------------------------------------------------
# tìm kiếm quản trị viên 
def searchAdmin():
    while True:
        print()
        AdminID = input("Nhập Mã Quản trị viên cần tìm: ").strip()
        mycursor.execute("SELECT * FROM AdminRecord WHERE AdminID = %s", (AdminID,))
        records = mycursor.fetchall()
        if records:
            for row in records:
                print("****************************** Kết quả tìm kiếm ******************************")
                print("\t Mã Quản trị viên:", row[0])
                print("\t Mật khẩu:", row[1])
                print()
        else:
            print("Không tìm thấy kết quả phù hợp.\n")

        ch = input("Bạn có muốn tìm thêm Quản trị viên khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break
    return

#---------------------------------------------------------------------------------------------------------
# cập nhật quản trị viên 
def updateAdmin():
    while True:
        print()
        AdminID = input("Nhập Mã Quản trị viên cần cập nhật: ").strip()
        mycursor.execute("SELECT * FROM AdminRecord WHERE AdminID = %s", (AdminID,))
        if not mycursor.fetchone():
            print("Không tìm thấy mã Quản trị viên này.\n")
            continue

        while True:
            NewPassword = input("Nhập Mật khẩu mới: ").strip()
            Confirm = input("Nhập lại Mật khẩu mới: ").strip()
            if NewPassword != Confirm:
                print("Hai mật khẩu không trùng khớp. Vui lòng thử lại.\n")
            else:
                break

        mycursor.execute("UPDATE AdminRecord SET Password = %s WHERE AdminID = %s", (NewPassword, AdminID))
        mydb.commit()
        print("Cập nhật mật khẩu thành công.\n")

        ch = input("Bạn có muốn cập nhật Quản trị viên khác không? [Yes/No]: ").strip().lower()
        if ch != "yes":
            break
    return
