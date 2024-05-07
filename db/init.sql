CREATE DATABASE IF NOT EXISTS Watcher;

USE Watcher;

CREATE TABLE IF NOT EXISTS Users(
	CodUser INT PRIMARY KEY AUTO_INCREMENT,
	Name Varchar(100) NOT NULL,
    Email Varchar(100) NOT NULL,
    Password Varchar(255) NOT NULL
);

-- INSERT INTO Users(
-- 	Name, 
--     Email,
--     Password
-- ) VALUES
-- 	('Tom Holland', 'tomholland@gmail.com', 'zendaya');

-- SELECT * FROM Users;



