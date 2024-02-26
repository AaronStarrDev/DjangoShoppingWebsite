--
-- 由SQLiteStudio v3.3.3 产生的文件 Sun Mar 20 17:01:08 2022
--
-- 文本编码：UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：sellerData
CREATE TABLE sellerData (ItemName TEXT NOT NULL, ID INT PRIMARY KEY NOT NULL UNIQUE, Stock INT, ImageName TEXT, Price DOUBLE NOT NULL, Class TEXT NOT NULL);
INSERT INTO sellerData (ItemName, ID, Stock, ImageName, Price, Class) VALUES ('Apple Airpods Max', 100, 10, 'max.png', 500.0, 'AirPods');
INSERT INTO sellerData (ItemName, ID, Stock, ImageName, Price, Class) VALUES ('iphone13', 101, 10, '13.png', 600.0, 'iPhone');

-- 表：userData
CREATE TABLE userData ("ID " INT PRIMARY KEY NOT NULL UNIQUE, Passward NOT NULL UNIQUE);
INSERT INTO userData ("ID ", Passward) VALUES ('admin', 123456);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
