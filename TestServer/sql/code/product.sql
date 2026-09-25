-- 1. Bảng Provider
CREATE TABLE Provider (
    Id UUID NOT NULL,
    name VARCHAR(192) NOT NULL,
    phone VARCHAR(20),
    CONSTRAINT PK_Provider PRIMARY KEY (Id)
);

-- 2. Bảng Categories
CREATE TABLE Categories (
    Id UUID NOT NULL,
    name VARCHAR(32) NOT NULL,
    CONSTRAINT PK_Categories PRIMARY KEY (Id)
);

-- 3. Bảng Product
CREATE TABLE Product (
    Id UUID NOT NULL,
    provider UUID NOT NULL,
    number INT,
    CONSTRAINT PK_Product PRIMARY KEY (Id),
    CONSTRAINT FK_Product_Provider FOREIGN KEY (provider) REFERENCES Provider(Id)
);

-- 4. Bảng Product_Categories
CREATE TABLE Product_Categories (
    product UUID NOT NULL,
    category UUID NOT NULL,
    CONSTRAINT PK_Product_Categories PRIMARY KEY (product, category),
    CONSTRAINT FK_ProductCategories_Product FOREIGN KEY (product) REFERENCES Product(Id) ON DELETE CASCADE,
    CONSTRAINT FK_ProductCategories_Category FOREIGN KEY (category) REFERENCES Categories(Id) ON DELETE CASCADE
);