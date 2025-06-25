import pymysql
from db_config import get_connection

class UserApp:
    def __init__(self):
        self.mydb = get_connection()
        self.mycursor = self.mydb.cursor()

    def displayUser(self):
        print("\nDanh sách người dùng:\n")
        self.mycursor.execute("SELECT UserID, UserName, Passwd FROM UserRecord")
        records = self.mycursor.fetchall()
        for idx, row in enumerate(records, 1):
            print(f"********** Người dùng số {idx} **********")
            print("Mã người dùng:", row[0])
            print("Tên người dùng:", row[1])
            print("Mật khẩu:", row[2])
            print()
        input("Nhấn Enter để quay lại...")

    def insertUser(self):
        while True:
            print()
            UserID = input("Nhập mã người dùng (ví dụ: FnB1234): ").strip()
            UserName = input("Nhập tên người dùng: ").strip()

            self.mycursor.execute("SELECT UserID FROM UserRecord WHERE UserID = %s", (UserID,))
            if self.mycursor.fetchone():
                print("Mã người dùng đã tồn tại.")
                continue

            while True:
                Password = input("Nhập mật khẩu: ").strip()
                Confirm = input("Nhập lại mật khẩu: ").strip()
                if Password != Confirm:
                    print("Mật khẩu không khớp.")
                else:
                    break

            try:
                self.mycursor.execute(
                    "INSERT INTO UserRecord (UserID, UserName, Passwd) VALUES (%s, %s, %s)",
                    (UserID, UserName, Password)
                )
                self.mydb.commit()
                print("Đã thêm người dùng.")
            except pymysql.MySQLError as e:
                print(f"Lỗi khi thêm người dùng: {e}")

            if input("Thêm người dùng khác? [yes/no]: ").strip().lower() != "yes":
                break

    def deleteUser(self):
        while True:
            UserID = input("\nNhập mã người dùng cần xóa: ").strip()
            self.mycursor.execute("SELECT * FROM UserRecord WHERE UserID = %s", (UserID,))
            if not self.mycursor.fetchone():
                print("Người dùng không tồn tại.")
            else:
                self.mycursor.execute("DELETE FROM UserRecord WHERE UserID = %s", (UserID,))
                self.mydb.commit()
                print("Đã xóa người dùng.")

            if input("Xóa người dùng khác? [yes/no]: ").strip().lower() != "yes":
                break

    def searchUser(self):
        while True:
            UserID = input("\nNhập mã người dùng cần tìm: ").strip()
            self.mycursor.execute("SELECT UserID, UserName, Passwd FROM UserRecord WHERE UserID = %s", (UserID,))
            record = self.mycursor.fetchone()
            if record:
                print("\n*** Kết quả tìm kiếm ***")
                print("Mã người dùng:", record[0])
                print("Tên người dùng:", record[1])
                print("Mật khẩu:", record[2])
            else:
                print("Không tìm thấy người dùng.")

            if input("Tìm người dùng khác? [yes/no]: ").strip().lower() != "yes":
                break

    def updateUser(self):
        while True:
            UserID = input("\nNhập mã người dùng cần cập nhật: ").strip()
            self.mycursor.execute("SELECT * FROM UserRecord WHERE UserID = %s", (UserID,))
            if not self.mycursor.fetchone():
                print("Người dùng không tồn tại.")
                continue

            UserName = input("Nhập tên mới: ").strip()
            while True:
                Password = input("Nhập mật khẩu mới: ").strip()
                Confirm = input("Nhập lại mật khẩu: ").strip()
                if Password != Confirm:
                    print("Mật khẩu không khớp.")
                else:
                    break

            self.mycursor.execute(
                "UPDATE UserRecord SET UserName = %s, Passwd = %s WHERE UserID = %s",
                (UserName, Password, UserID)
            )
            self.mydb.commit()
            print("Cập nhật thành công.")

            if input("Cập nhật người dùng khác? [yes/no]: ").strip().lower() != "yes":
                break
