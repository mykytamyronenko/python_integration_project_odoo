DROP TABLE IF EXISTS users, products, customers, suppliers,
purchase_orders, sale_orders, stock_movements, purchase_order_lines, sale_order_lines, invoices;


CREATE TABLE users (
    id_users INT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(320) NOT NULL,
    phone_number VARCHAR(30) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT pk_users PRIMARY KEY (id_users),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT uq_users_phone_number UNIQUE (phone_number),
    CONSTRAINT ck_users_email_format CHECK (email ~* '^[A-Z0-9._+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'),
    CONSTRAINT ck_users_role CHECK (role IN ('ADMIN', 'USER'))
);


CREATE TABLE products (
    id_products INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    reference VARCHAR(50) NOT NULL,
    purchase_price NUMERIC(12,2) NOT NULL,
    sale_price NUMERIC(12,2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
 
    CONSTRAINT pk_products PRIMARY KEY (id_products),
    CONSTRAINT uq_products_reference UNIQUE (reference),
    CONSTRAINT ck_products_purchase_price CHECK (purchase_price >= 0),
    CONSTRAINT ck_products_sale_price CHECK (sale_price >= 0),
    CONSTRAINT ck_products_stock_quantity CHECK (stock_quantity >= 0)
);


CREATE TABLE customers (
    id_customers INT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(320) NOT NULL,
    phone_number VARCHAR(30) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
    CONSTRAINT pk_customers PRIMARY KEY (id_customers),
    CONSTRAINT uq_customers_email UNIQUE (email),
    CONSTRAINT uq_customers_phone_number UNIQUE (phone_number),
    CONSTRAINT ck_customers_email_format CHECK (email ~* '^[A-Z0-9._+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$')
);


CREATE TABLE suppliers (
    id_suppliers INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(320) NOT NULL,
    phone_number VARCHAR(30) NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
    CONSTRAINT pk_suppliers PRIMARY KEY (id_suppliers),
    CONSTRAINT uq_suppliers_name UNIQUE (name),
    CONSTRAINT uq_suppliers_email UNIQUE (email),
    CONSTRAINT uq_suppliers_phone_number UNIQUE (phone_number),
    CONSTRAINT ck_suppliers_email_format CHECK (email ~* '^[A-Z0-9._+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$')
);


CREATE TABLE purchase_orders (
    id_purchase_orders INT GENERATED ALWAYS AS IDENTITY,
    users_id INT NOT NULL,
    suppliers_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ORDERED',
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT pk_purchase_orders PRIMARY KEY (id_purchase_orders),
    CONSTRAINT fk_purchase_orders_user
        FOREIGN KEY (users_id) REFERENCES users (id_users)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_purchase_orders_supplier
        FOREIGN KEY (suppliers_id) REFERENCES suppliers (id_suppliers)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_purchase_orders_status
        CHECK (status IN ('ORDERED', 'RECEIVED', 'CANCELLED')),
    CONSTRAINT ck_purchase_orders_total CHECK (total_amount >= 0)
);


CREATE TABLE sale_orders (
    id_sale_orders INT GENERATED ALWAYS AS IDENTITY,
    customers_id INT NOT NULL,
    users_id INT NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT pk_sale_orders PRIMARY KEY (id_sale_orders),
    CONSTRAINT fk_sale_orders_customer
        FOREIGN KEY (customers_id) REFERENCES customers (id_customers)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_sale_orders_user
        FOREIGN KEY (users_id) REFERENCES users (id_users)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_sale_orders_total CHECK (total_amount >= 0)
);


CREATE TABLE stock_movements (
    id_stock_movements INT GENERATED ALWAYS AS IDENTITY,
    products_id INT NOT NULL,
    users_id INT NOT NULL,
    quantity INT NOT NULL,
    movement_type VARCHAR(30) NOT NULL,
    movement_date DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT pk_stock_movements PRIMARY KEY (id_stock_movements),
    CONSTRAINT fk_stock_movements_product
        FOREIGN KEY (products_id) REFERENCES products (id_products)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_stock_movements_user
        FOREIGN KEY (users_id) REFERENCES users (id_users)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_stock_movements_quantity CHECK (quantity > 0),
    CONSTRAINT ck_stock_movements_type CHECK (movement_type IN ('IN', 'OUT'))
);


CREATE TABLE purchase_order_lines (
    id_purchase_order_lines INT GENERATED ALWAYS AS IDENTITY,
    purchase_orders_id INT NOT NULL,
    products_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    subtotal NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,

    CONSTRAINT pk_purchase_order_lines PRIMARY KEY (id_purchase_order_lines),
    CONSTRAINT fk_pol_purchase_order
        FOREIGN KEY (purchase_orders_id) REFERENCES purchase_orders (id_purchase_orders)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pol_product
        FOREIGN KEY (products_id) REFERENCES products (id_products)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_pol_quantity CHECK (quantity > 0),
    CONSTRAINT ck_pol_unit_price CHECK (unit_price >= 0)
);


CREATE TABLE sale_order_lines (
    id_sale_order_lines INT GENERATED ALWAYS AS IDENTITY,
    sales_orders_id INT NOT NULL,
    products_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    subtotal NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,

    CONSTRAINT pk_sale_order_lines PRIMARY KEY (id_sale_order_lines),
    CONSTRAINT fk_sol_sale_order
        FOREIGN KEY (sales_orders_id) REFERENCES sale_orders (id_sale_orders)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_sol_product
        FOREIGN KEY (products_id) REFERENCES products (id_products)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_sol_quantity CHECK (quantity > 0),
    CONSTRAINT ck_sol_unit_price CHECK (unit_price >= 0)
);


CREATE TABLE invoices (
    id_invoices INT GENERATED ALWAYS AS IDENTITY,
    invoice_number VARCHAR(50) NOT NULL,
    sales_orders_id INT NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,

    CONSTRAINT pk_invoices PRIMARY KEY (id_invoices),
    CONSTRAINT uq_invoices_invoice_number UNIQUE (invoice_number),
    CONSTRAINT uq_invoices_sales_order UNIQUE (sales_orders_id),
    CONSTRAINT fk_invoices_sale_order
        FOREIGN KEY (sales_orders_id) REFERENCES sale_orders (id_sale_orders)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_invoices_status
        CHECK (status IN ('PENDING', 'PAID', 'OVERDUE', 'CANCELLED')),
    CONSTRAINT ck_invoices_total CHECK (total_amount >= 0),
    CONSTRAINT ck_invoices_dates CHECK (due_date >= invoice_date)
);



-------------------------------------------
-------------------------------------------



INSERT INTO users (first_name, last_name, email, phone_number, password_hash, role) VALUES
('Camille', 'Dupont', 'camille.dupont@stockpro.be', '+32 470 11 11 11', '$2b$12$Gnzo2YVDWfvXfw1BG6v0Oefa6z1cQEY8TlgvpiH1n.4uSn.Eh2o7O', 'ADMIN'),
('Lucas', 'Martin', 'lucas.martin@stockpro.be', '+32 470 22 22 22', '$2b$12$f1sXXanygiId7/4MnjDk3egrIKd9cfnz4ps/BBWYuZ5dvzf2Bt8Ui', 'USER'),
('Emma', 'Leroy', 'emma.leroy@stockpro.be', '+32 470 33 33 33', '$2b$12$1zrvFahUU/juUhFY2g.JRua785uBZCK27Ez7lBt5euyHGHrvioC6q', 'USER'),
('Noah', 'Peeters', 'noah.peeters@stockpro.be', '+32 470 44 44 44', '$2b$12$ki/I7NnH.lnXdnMrHJJgSeE3rMCBLQCvlbfaTwgV8MBFAL/pFz5XO', 'USER');
 

INSERT INTO suppliers (name, email, phone_number, city) VALUES
('TechDistrib', 'contact@techdistrib.be', '+32 2 555 01 01', 'Bruxelles'),
('Global Components', 'sales@globalcomponents.eu', '+32 3 555 02 02', 'Anvers'),
('Office Plus', 'info@officeplus.be', '+32 4 555 03 03', 'Liège');
 

INSERT INTO products (name, reference, purchase_price, sale_price, stock_quantity) VALUES
('Clavier mécanique', 'KB-MECH-001',  45.00, 79.90, 17),
('Souris sans fil', 'MS-WL-002', 12.00, 24.90, 28),
('Écran 24" Full HD', 'MN-24-003', 95.00, 149.00, 7),
('Écran 27" QHD', 'MN-27-004',   180.00, 269.00, 5),
('Casque audio USB', 'HS-USB-005', 28.00, 54.90, 12),
('Webcam HD 1080p', 'WC-HD-006', 22.00, 44.90, 0),
('Hub USB-C 7 ports', 'HB-UC-007', 18.00, 39.90, 16),
('Disque SSD 1 To', 'SD-1TB-008', 55.00,  94.90, 13),
('Câble HDMI 2 m', 'CB-HD-009', 3.00, 9.90, 0),
('Chaise de bureau ergonomique', 'CH-ERG-010', 110.00, 199.00, 6);
 

INSERT INTO customers (first_name, last_name, email, phone_number, address, city, postal_code) VALUES
('Sophie', 'Lambert', 'sophie.lambert@example.com', '+32 475 10 10 10', 'Rue de la Loi 12', 'Bruxelles', '1000'),
('Thomas', 'Dubois', 'thomas.dubois@example.com', '+32 475 20 20 20', 'Avenue Louise 45', 'Bruxelles', '1050'),
('Julie',  'Claes', 'julie.claes@example.com', '+32 475 30 30 30', 'Rue Neuve 8', 'Liège', '4000'),
('Antoine','Janssens', 'antoine.janssens@example.com', '+32 475 40 40 40', 'Meir 22', 'Anvers', '2000'),
('Laura',  'Maes', 'laura.maes@example.com', '+32 475 50 50 50', 'Korenmarkt 5', 'Gand', '9000'),
('Maxime', 'Renard', 'maxime.renard@example.com', '+32 475 60 60 60', 'Rue de Fer 17', 'Namur', '5000'),
('Chloé',  'Vandenberghe', 'chloe.vandenberghe@example.com','+32 475 70 70 70','Grand-Place 3', 'Mons', '7000');
 

INSERT INTO purchase_orders (users_id, suppliers_id, status, total_amount, order_date) VALUES
(1, 1, 'RECEIVED', 1620.00, '2026-09-02'),
(2, 2, 'RECEIVED', 2855.00, '2026-09-15'),
(1, 3, 'RECEIVED', 1300.00, '2026-10-01'),
(3, 1, 'ORDERED',   414.00, '2026-10-28'),
(2, 2, 'CANCELLED', 720.00, '2026-10-10');
 

INSERT INTO purchase_order_lines (purchase_orders_id, products_id, quantity, unit_price) VALUES
(1, 1, 20, 45.00),
(1, 2, 30, 12.00),
(1, 7, 20, 18.00),
(2, 3, 10, 95.00),
(2, 4, 6, 180.00),
(2, 8, 15, 55.00),
(3, 10, 8, 110.00),
(3, 5, 15, 28.00),
(4, 6, 12, 22.00),
(4, 9, 50, 3.00),
(5, 4, 4, 180.00);
 

INSERT INTO sale_orders (customers_id, users_id, total_amount, order_date) VALUES
(1, 2, 209.60, '2026-09-20'),
(2, 3, 337.90, '2026-09-28'),
(3, 2, 458.80, '2026-10-05'),
(4, 4, 452.90, '2026-10-14'),
(5, 3, 309.40, '2026-10-22'),
(1, 2, 149.00, '2026-11-03');
 

INSERT INTO sale_order_lines (sales_orders_id, products_id, quantity, unit_price) VALUES
(1, 1, 2, 79.90),
(1, 2, 2, 24.90),
(2, 3, 2, 149.00),
(2, 7, 1, 39.90),
(3, 4, 1, 269.00),
(3, 8, 2, 94.90),
(4, 10, 2, 199.00),
(4, 5, 1, 54.90),
(5, 1, 1, 79.90),
(5, 5, 2, 54.90),
(5, 7, 3, 39.90),
(6, 3, 1, 149.00);
 

INSERT INTO invoices (invoice_number, sales_orders_id, total_amount, status, invoice_date, due_date) VALUES
('INV-2026-0001', 1, 209.60, 'PAID', '2026-09-20', '2026-10-20'),
('INV-2026-0002', 2, 337.90, 'PAID', '2026-09-28', '2026-10-28'),
('INV-2026-0003', 3, 458.80, 'OVERDUE', '2026-10-05', '2026-11-04'),
('INV-2026-0004', 4, 452.90, 'PENDING', '2026-10-14', '2026-11-13'),
('INV-2026-0005', 5, 309.40, 'PENDING', '2026-10-22', '2026-11-21');
 

INSERT INTO stock_movements (products_id, users_id, quantity, movement_type, movement_date) VALUES
( 1, 1, 20, 'IN', '2026-09-05'),
( 2, 1, 30, 'IN', '2026-09-05'),
( 7, 1, 20, 'IN', '2026-09-05'),
( 3, 2, 10, 'IN', '2026-09-18'),
( 4, 2, 6, 'IN', '2026-09-18'),
( 8, 2, 15, 'IN', '2026-09-18'),
(10, 1, 8, 'IN', '2026-10-04'),
( 5, 1, 15, 'IN', '2026-10-04'),
( 1, 2, 2, 'OUT', '2026-09-20'),
( 2, 2, 2, 'OUT', '2026-09-20'),
( 3, 3, 2, 'OUT', '2026-09-28'),
( 7, 3, 1, 'OUT', '2026-09-28'),
( 4, 2, 1, 'OUT', '2026-10-05'),
( 8, 2, 2, 'OUT', '2026-10-05'),
(10, 4, 2, 'OUT', '2026-10-14'),
( 5, 4, 1, 'OUT', '2026-10-14'),
( 1, 3, 1, 'OUT', '2026-10-22'),
( 5, 3, 2, 'OUT', '2026-10-22'),
( 7, 3, 3, 'OUT', '2026-10-22'),
( 3, 2, 1, 'OUT', '2026-11-03');