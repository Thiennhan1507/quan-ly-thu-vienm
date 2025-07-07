-- Tạo cơ sở dữ liệu nếu chưa có
CREATE DATABASE IF NOT EXISTS Library;
USE Library;

-- Tạo bảng BookRecord
CREATE TABLE IF NOT EXISTS BookRecord (
    BookID VARCHAR(10) PRIMARY KEY,
    BookName VARCHAR(50),
    Author VARCHAR(50),
    PublisherYear INT,
    quantity INT DEFAULT 0 
);

-- Tạo bảng UserRecord
CREATE TABLE IF NOT EXISTS UserRecord (
    UserID VARCHAR(20) PRIMARY KEY,
    UserName VARCHAR(30) NOT NULL,
    Passwd VARCHAR(50) NOT NULL,
    Fullname VARCHAR(50) NOT NULL,
    BookID VARCHAR(10),
);

-- Tạo bảng AdminRecord
CREATE TABLE IF NOT EXISTS AdminRecord (
    AdminID VARCHAR(20) PRIMARY KEY,
    Passwd  VARCHAR(50)
);

-- Tài khoản cho admin 
INSERT INTO AdminRecord
VALUES  ("fnbtoinv", 123456789), 
		("fnbdatpt", 123456789),
        ("fnbduongnk",123456789),
        ("fnbkhanhhq",123456789),
        ("fnbnhannt",123456789);

-- Tạo bảng Feedback
CREATE TABLE IF NOT EXISTS Feedback (
	FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    Feedback TEXT,
    Rating INT,
    CONSTRAINT check_rating CHECK (Rating >= 0 AND Rating <= 10) 
);

-- bảng giao dịch mượn/trả
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    book_id VARCHAR(10) NOT NULL,
    borrow_date DATE,
    due_date DATE,
    return_date DATE,
    status ENUM('đang mượn', 'đã trả', 'quá hạn'),
    FOREIGN KEY (book_id) REFERENCES BookRecord(BookID) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES UserRecord(UserID) ON DELETE CASCADE
);

