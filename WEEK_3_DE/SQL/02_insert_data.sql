USE celebal_week3;

-- Insert data into Customers table

INSERT INTO customers (
    customer_id,
    customer_name,
    segment,
    country,
    city,
    state,
    postal_code,
    region
)
SELECT DISTINCT
    customer_id,
    customer_name,
    segment,
    country,
    city,
    state,
    postal_code,
    region
FROM superstore_raw;

-- Insert data into Products table

INSERT INTO products (
    product_id,
    product_name,
    category,
    sub_category
)
SELECT DISTINCT
    product_id,
    product_name,
    category,
    sub_category
FROM superstore_raw;

-- Insert data into Orders table

INSERT INTO orders (
    row_id,
    order_id,
    order_date,
    ship_date,
    ship_mode,
    customer_id,
    product_id,
    sales,
    quantity,
    discount,
    profit
)
SELECT DISTINCT
    CAST(row_id AS UNSIGNED),
    order_id,
    order_date,
    ship_date,
    ship_mode,
    customer_id,
    product_id,
    CAST(sales AS DECIMAL(12,4)),
    CAST(quantity AS UNSIGNED),
    CAST(discount AS DECIMAL(6,4)),
    CAST(profit AS DECIMAL(12,4))
FROM superstore_raw;

-- Verify records

SELECT COUNT(*) AS total_customers
FROM customers;

SELECT COUNT(*) AS total_products
FROM products;

SELECT COUNT(*) AS total_orders
FROM orders;