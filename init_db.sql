-- Tạo cơ sở dữ liệu nếu chưa có
CREATE DATABASE IF NOT EXISTS Library;
USE Library;

-- Tạo bảng BookRecord
CREATE TABLE IF NOT EXISTS BookRecord (
    BookID VARCHAR(10) PRIMARY KEY,
    BookName VARCHAR(50),
    Author VARCHAR(30),
    Publisher VARCHAR(30)
);

-- Tạo bảng UserRecord
CREATE TABLE IF NOT EXISTS UserRecord (
    UserID VARCHAR(20) PRIMARY KEY,
    UserName VARCHAR(30) NOT NULL,
    Passwd VARCHAR(50) NOT NULL,
    Fullname VARCHAR(50) NOT NULL,
    BookID VARCHAR(10),
    FOREIGN KEY (BookID) REFERENCES BookRecord(BookID) ON DELETE SET NULL ON UPDATE CASCADE -- thêm ràng buộc ON DELETE SET NULL trong khóa ngoại để tránh lỗi khi xóa sách
);

-- Tạo bảng AdminRecord
CREATE TABLE IF NOT EXISTS AdminRecord (
    AdminID VARCHAR(20) PRIMARY KEY,
    Passwd  VARCHAR(50)
);

-- Tạo bảng Feedback
CREATE TABLE IF NOT EXISTS Feedback (
	FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    Feedback TEXT,
    Rating INT,
    CONSTRAINT check_rating CHECK (Rating >= 0 AND Rating <= 10) 
);


