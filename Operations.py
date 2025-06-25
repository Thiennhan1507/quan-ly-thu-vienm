import Book
import User
import Admin
from db_config import get_connection

#----------------------------------------------------------------------------------------
# Chức năng dành cho Menu Quản trị viên

def BookManagement():
    while True:
        print("\t\t\t Quản lý Hồ sơ Sách\n")
        print("==============================================================")
        print("1. Thêm hồ sơ sách")
        print("2. Hiển thị danh sách sách")
        print("3. Tìm kiếm sách")
        print("4. Xóa hồ sơ sách")
        print("5. Cập nhật hồ sơ sách")
        print("6. Quay lại Menu chính")
        #print(7)
        #print(8)
        print("===============================================================")
        

        choice = int(input("Nhập lựa chọn từ 1 đến 6 -------> : "))
        if choice == 1:
            Book.insertBook()
        elif choice == 2:
            Book.displayBook()
        elif choice == 3:
            Book.searchBook()
        elif choice == 4:
            Book.deleteBook()
        elif choice == 5:
            Book.updateBook()
        elif choice == 6:
            return
        else:
            print("Lựa chọn không hợp lệ......Vui lòng nhập lại lựa chọn của bạn")
            x = input("Nhấn Enter để tiếp tục")

#----------------------------------------------------------------------------------------
def UserManagement():
    while True:
        print("\t\t\t Quản lý Hồ sơ Người dùng\n")
        print("==============================================================")
        print("1. Thêm hồ sơ người dùng")
        print("2. Hiển thị danh sách người dùng")
        print("3. Tìm kiếm người dùng")
        print("4. Xóa hồ sơ người dùng")
        print("5. Cập nhật hồ sơ người dùng")
        print("6. Quay lại Menu chính")
        print("===============================================================")
        choice = int(input("Nhập lựa chọn từ 1 đến 6 -------> : "))
        if choice == 1:
            User.insertUser()
        elif choice == 2:
            User.displayUser()
        elif choice == 3:
            User.searchUser()
        elif choice == 4:
            User.deleteUser()
        elif choice == 5:
            User.updateUser()
        elif choice == 6:
            return
        else:
            print("Lựa chọn không hợp lệ......Vui lòng nhập lại lựa chọn của bạn")
            x = input("Nhấn Enter để tiếp tục")

#----------------------------------------------------------------------------------------
# quản lý hồ sơ quản trị viên 
def AdminManagement():
    while True:
        print("\t\t\t Quản lý Hồ sơ Quản trị viên\n")
        print("==============================================================")
        print("1. Thêm hồ sơ quản trị viên")
        print("2. Hiển thị danh sách quản trị viên")
        print("3. Tìm kiếm quản trị viên")
        print("4. Xóa hồ sơ quản trị viên")
        print("5. Cập nhật hồ sơ quản trị viên")
        print("6. Quay lại Menu chính")
        print("===============================================================")
        choice = int(input("Nhập lựa chọn từ 1 đến 6 -------> : "))
        if choice == 1:
            Admin.insertAdmin()
        elif choice == 2:
            Admin.displayAdmin()
        elif choice == 3:
            Admin.searchAdmin()
        elif choice == 4:
            Admin.deleteAdmin()
        elif choice == 5:
            Admin.updateAdmin()
        elif choice == 6:
            return
        else:
            print("Lựa chọn không hợp lệ......Vui lòng nhập lại lựa chọn của bạn")
            x = input("Nhấn Enter để tiếp tục")

#----------------------------------------------------------------------------------------
# góp ý và đánh giá của khách hàng 
def FeedbackTable():
    print()
    print("Bảng Góp ý và Đánh giá: \n")
    mycursor.execute("SELECT * from Feedback")
    records = mycursor.fetchall()
    row_no = 0
    for rows in records:
        row_no += 1
        print("******************************", "Hàng số", row_no, "******************************")
        print("\t             Góp ý: ", rows[0])
        print("\t      Đánh giá (tối đa 10 điểm): ", rows[1])
        print()

#----------------------------------------------------------------------------------------
# Chức năng Menu Người dùng

def BookCentre():
    while True:
        print("\t\t\t Trung tâm Sách \n")
        print("==============================================================")
        print("1. Danh sách tất cả sách")
        print("2. Mượn sách")
        print("3. Hiển thị sách đã mượn")
        print("4. Trả sách đã mượn")
        print("5. Quay lại Menu chính")
        print("===============================================================")
        choice = int(input("Nhập lựa chọn từ 1 đến 5 -------> : "))
        if choice == 1:
            Book.BookList()
        elif choice == 2:
            Book.IssueBook()
        elif choice == 3:
            Book.ShowIssuedBook()
        elif choice == 4:
            Book.returnBook()
        elif choice == 5:
            return
        else:
            print("Lựa chọn không hợp lệ......Vui lòng nhập lại lựa chọn của bạn")
            x = input("Nhấn Enter để tiếp tục")

#----------------------------------------------------------------------------------------
# góp ý và đánh giá 
def Feedback():
    while True:
        data = ()
        print("\t\t\t Góp ý và Đánh giá\n")
        print("==============================================================")
        Feedback = input("Hãy nhập góp ý của bạn về Thư viện và cho biết chúng tôi có thể cải thiện điều gì để làm bạn hài lòng hơn!! :)) ----> ")
        Ratings = input("Đánh giá chúng tôi trên thang điểm 10: ")
        data = (Feedback, Ratings)
        query = "INSERT INTO Feedback (Feedback, Rating) VALUES (%s, %s)"
        mycursor.execute(query, data)
        mydb.commit()
        print()
        print("Cảm ơn bạn vì những góp ý quý giá!")
        return      

#----------------------------------------------------------------------------------------
mydb = get_connection()
mycursor = mydb.cursor()

