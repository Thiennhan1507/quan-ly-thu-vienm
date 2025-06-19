-- Tạo cơ sở dữ liệu nếu chưa có
CREATE DATABASE IF NOT EXISTS Library;
USE Library;

-- Tạo bảng BookRecord
CREATE TABLE IF NOT EXISTS BookRecord (
    BookID VARCHAR(10) PRIMARY KEY,
    BookName VARCHAR(35),
    Author VARCHAR(30),
    Publisher VARCHAR(30)
);

-- Tạo bảng UserRecord
CREATE TABLE IF NOT EXISTS UserRecord (
    UserID VARCHAR(10) PRIMARY KEY,
    UserName VARCHAR(20),
    Password VARCHAR(20),
    BookID VARCHAR(10),
    FOREIGN KEY (BookID) REFERENCES BookRecord(BookID)
);

-- Chèn dữ liệu mẫu vào UserRecord
INSERT INTO UserRecord (UserID, UserName, Password, BookID) VALUES
    ('101', 'Kunal', '1234', NULL),
    ('102', 'Vishal', '3050', NULL),
    ('103', 'Siddhesh', '5010', NULL);

-- Tạo bảng AdminRecord
CREATE TABLE IF NOT EXISTS AdminRecord (
    AdminID VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(20)
);

-- Chèn dữ liệu mẫu vào AdminRecord
INSERT INTO AdminRecord (AdminID, Password) VALUES
    ('Kunal1020', '123'),
    ('Siddesh510', '786'),
    ('Vishal305', '675');

-- Tạo bảng Feedback
CREATE TABLE IF NOT EXISTS Feedback (
    Feedback VARCHAR(100) PRIMARY KEY,
    Rating VARCHAR(10)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);