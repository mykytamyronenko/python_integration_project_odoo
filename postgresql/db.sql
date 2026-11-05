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


-- CREATE TABLE purchase_orders (
--     id_purchase_orders INT GENERATED ALWAYS AS IDENTITY,
--     users_id INT NOT NULL,
--     suppliers_id INT NOT NULL,
--     status VARCHAR(30) NOT NULL DEFAULT 'DRAFT',
--     total_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
--     order_date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
--     CONSTRAINT pk_purchase_orders PRIMARY KEY (id_purchase_orders),
--     CONSTRAINT fk_purchase_orders_user
--         FOREIGN KEY (users_id) REFERENCES users (id_users)
--         ON UPDATE CASCADE ON DELETE RESTRICT,
--     CONSTRAINT fk_purchase_orders_supplier
--         FOREIGN KEY (suppliers_id) REFERENCES suppliers (id_suppliers)
--         ON UPDATE CASCADE ON DELETE RESTRICT,
--     CONSTRAINT ck_purchase_orders_status
--         CHECK (status IN ('DRAFT', 'ORDERED', 'RECEIVED', 'CANCELLED')),
--     CONSTRAINT ck_purchase_orders_total CHECK (total_amount >= 0)
-- );
 
-- CREATE INDEX idx_purchase_orders_user ON purchase_orders (users_id);
-- CREATE INDEX idx_purchase_orders_supplier ON purchase_orders (suppliers_id);