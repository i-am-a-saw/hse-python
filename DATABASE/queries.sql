-- Создание таблиц

CREATE PROCEDURE create_producers()
    BEGIN
        CREATE TABLE IF NOT EXISTS Producers (
                    producer_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(200) NOT NULL,
                    country VARCHAR(200) NOT NULL,
                    total_amount INT,
                    UNIQUE(name, country)  
                );
    END;

CREATE PROCEDURE create_beer_types()
    BEGIN
        CREATE TABLE IF NOT EXISTS BeerTypes (
            beer_type_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(200) NOT NULL,
            alcohol_content REAL NOT NULL,
            producer_id INT
        );
    END;

CREATE PROCEDURE create_bottles()
    BEGIN
        CREATE TABLE IF NOT EXISTS Bottles (
            bottle_id INT PRIMARY KEY AUTO_INCREMENT,
            beer_name VARCHAR(200),
            volume REAL NOT NULL,
            price REAL NOT NULL,
            producer_name VARCHAR(200)
        );
    END;

CREATE PROCEDURE create_sales()
    BEGIN
        CREATE TABLE IF NOT EXISTS Sales (
            sale_id INT PRIMARY KEY AUTO_INCREMENT,
            bottle_id INT,
            beer_type_id REAL NOT NULL,
            cost INTEGER,
            date DATE
        );
    END;


-----------------------------------------
-- Создание триггера на поле total_amount
-----------------------------------------

CREATE TRIGGER IF NOT EXISTS update_total_price()
            AFTER INSERT ON Bottles
            FOR EACH ROW
            BEGIN
                UPDATE Producers
                SET total_amount = total_amount + NEW.price
                WHERE name = NEW.producer_name;
            END;


----------------------------------
-- Добавление и удаление сущностей
----------------------------------

CREATE PROCEDURE AddProducer(
                IN p_name VARCHAR(255),
                IN p_country VARCHAR(255),
                IN p_total_price INT
            )
            BEGIN
                INSERT INTO Producers (name, country, total_price)
                VALUES (p_name, p_country, p_total_price);
            END;

CREATE PROCEDURE IF NOT EXISTS LoadProducers()
            BEGIN
                SELECT * FROM Producers;
            END;

CREATE PROCEDURE DeleteProducer(
                IN p_producer_name VARCHAR(200)
            )
            BEGIN
                DELETE FROM Producers
                WHERE name = p_producer_name;
            END;

CREATE PROCEDURE ResetIDsProducers()
            BEGIN
                CREATE TABLE IF NOT EXISTS TempProducers (
                    producer_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(200) NOT NULL,
                    country VARCHAR(200) NOT NULL,
                    total_amount INT,
                    UNIQUE(name, country)  
                );

                INSERT INTO TempProducers (name, country, total_amount) SELECT name, country, total_amount FROM Producers;
                DROP TABLE Producers;
                ALTER TABLE TempProducers RENAME TO Producers;
            END;



CREATE PROCEDURE AddBeerType(
                IN p_name VARCHAR(255),
                IN p_alcohol REAL,
                IN p_producer_id INT
            )
            BEGIN
                INSERT INTO BeerTypes (name, alcohol_content, producer_id)
                VALUES (p_name, p_alcohol, p_producer_id);
            END;
            
CREATE PROCEDURE IF NOT EXISTS LoadBeerTypes()
            BEGIN
                SELECT * FROM BeerTypes;
            END;

CREATE PROCEDURE DeleteBeerType(
                IN p_beer_name VARCHAR(200)
            )
            BEGIN
                DELETE FROM BeerTypes
                WHERE name = p_beer_name;
            END;

CREATE PROCEDURE ResetIDsBeerTypes()
            BEGIN
                CREATE TABLE IF NOT EXISTS TempBeerTypes (
                    beer_type_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(200) NOT NULL,
                    alcohol_content REAL NOT NULL,
                    producer_id INT 
                );

                INSERT INTO TempBeerTypes (name, alcohol_content, producer_id) SELECT name, alcohol_content, producer_id FROM BeerTypes;
                DROP TABLE BeerTypes;
                ALTER TABLE TempBeerTypes RENAME TO BeerTypes;
            END;



CREATE PROCEDURE AddSale(
                IN p_bottle_id INT,
                IN p_beer_type_id INT,
                IN p_cost INT,
                IN p_date DATE
            )
            BEGIN
                INSERT INTO SALES (bottle_id, beer_type_id, cost, date)
                VALUES (p_bottle_id, p_beer_type_id, p_cost, DATE(p_date));
            END;
            
CREATE PROCEDURE LoadSales()
            BEGIN
                SELECT * FROM Sales;
            END;

CREATE PROCEDURE DeleteSale(
                IN p_sale_id INT
            )
            BEGIN
                DELETE FROM Sales
                WHERE sale_id = p_sale_id;
            END;

CREATE PROCEDURE ResetIDsSales()
            BEGIN
                CREATE TABLE IF NOT EXISTS TempSales (
                    sale_id INT PRIMARY KEY AUTO_INCREMENT,
                    bottle_id INT,
                    beer_type_id REAL NOT NULL,
                    cost INTEGER,
                    date DATE
                );

                INSERT INTO TempSales (bottle_id, beer_type_id, cost, date) SELECT bottle_id, beer_type_id, cost, date FROM Sales;
                DROP TABLE Sales;
                ALTER TABLE TempSales RENAME TO Sales;
            END;


CREATE PROCEDURE AddBottle(
                IN p_beer_name VARCHAR(200),
                IN p_volume INT,
                IN p_price INT,
                IN p_producer_name VARCHAR(200)
            )
            BEGIN
                INSERT INTO Bottles (beer_name, volume, price, producer_name)
                VALUES (p_beer_name, p_volume, p_price, p_producer_name);
            END;
            
CREATE PROCEDURE LoadBottles()
            BEGIN
                SELECT * FROM Bottles;
            END;

CREATE PROCEDURE DeleteBottle(
                IN p_bottle_id INT
            )
            BEGIN
                DELETE FROM Bottles
                WHERE bottle_id = p_bottle_id;
            END;

CREATE PROCEDURE ResetIDsBottles()
            BEGIN
                CREATE TABLE IF NOT EXISTS TempBottles (
                    bottle_id INT PRIMARY KEY AUTO_INCREMENT,
                    beer_name VARCHAR(200),
                    volume REAL NOT NULL,
                    price REAL NOT NULL,
                    producer_name VARCHAR(200)
                );

                INSERT INTO TempBottles (beer_name, volume, price, producer_name) SELECT beer_name, volume, price, producer_name FROM Bottles;
                DROP TABLE Bottles;
                ALTER TABLE TempBottles RENAME TO Bottles;
            END;

-------------------------------------
-- Поиск сущностей
-------------------------------------



CREATE PROCEDURE SearchProducer(
                IN p_prod_name VARCHAR(200)
            )
            BEGIN
                SELECT * FROM Producers WHERE name LIKE p_prod_name;
            END;


CREATE PROCEDURE SearchBeerType(
                IN name_bt VARCHAR(200)
            )
            BEGIN
                SELECT * FROM BeerTypes WHERE name LIKE name_bt;
            END;

CREATE PROCEDURE SearchBottle(
                IN p_prod_name VARCHAR(200)
            )
            BEGIN
                SELECT * FROM Bottles WHERE beer_name LIKE p_prod_name;
            END;

CREATE PROCEDURE SearchSale(
                IN bottleid INT
            )
            BEGIN
                SELECT * FROM Sales WHERE bottle_id LIKE bottleid;
            END;



---------------------------------------
-- Удаление по неключевым полям
---------------------------------------


CREATE PROCEDURE DeleteBottleName(
                IN bid VARCHAR(200)
            )
            BEGIN
                DELETE FROM Bottles WHERE beer_name = bid;
            END;

    
CREATE PROCEDURE DeleteSaleID(
                IN bid INT
            )
            BEGIN
                DELETE FROM Sales WHERE bottle_id = bid;
            END;


------------------------------------------
-- Очищение таблиц
------------------------------------------


CREATE PROCEDURE IF NOT EXISTS ClearSales()
            BEGIN
                DROP TABLE Sales;
                CREATE TABLE Sales (
                    sale_id INT PRIMARY KEY AUTO_INCREMENT,
                    bottle_id INT,
                    beer_type_id REAL NOT NULL,
                    cost INTEGER,
                    date DATE
                );
            END;


CREATE PROCEDURE IF NOT EXISTS ClearBottles()
            BEGIN
                DROP TABLE Bottles;
                CREATE TABLE Bottles (
                    bottle_id INT PRIMARY KEY AUTO_INCREMENT,
                    beer_name VARCHAR(200),
                    volume REAL NOT NULL,
                    price REAL NOT NULL,
                    producer_name VARCHAR(200)
                );
            END;

CREATE PROCEDURE IF NOT EXISTS ClearBeerTypes()
            BEGIN
                DROP TABLE BeerTypes;
                CREATE TABLE BeerTypes (
                    beer_type_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(200) NOT NULL,
                    alcohol_content REAL NOT NULL,
                    producer_id INT
                );
            END;

CREATE PROCEDURE IF NOT EXISTS ClearProducers()
            BEGIN
                DROP TABLE Producers;
                CREATE TABLE Producers (
                    producer_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(200) NOT NULL,
                    country VARCHAR(200) NOT NULL,
                    total_amount INT,
                    UNIQUE(name, country)
                );
            END;













            
