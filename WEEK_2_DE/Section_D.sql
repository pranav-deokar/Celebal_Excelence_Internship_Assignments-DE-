-- ============================================================
-- Celebal Technologies Summer Internship 2026
-- Week 2 Assignment
-- Section D: JOINS & RELATIONSHIPS
-- Dataset: Sample Superstore
-- Author: Pranav Deokar
-- ============================================================



-- Select database
USE shopease_db;


-- Q19. INNER JOIN
-- Display order details with customer names

SELECT 
    o.order_id,
    o.order_date,
    c.first_name,
    c.last_name,
    o.total_amount
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id;



-- Q20. LEFT JOIN
-- Show all customers and their orders (if any)
-- Customers without orders will show NULL


SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;



-- Q21. JOIN across three tables
-- orders → order_items → products

SELECT 
    o.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct
FROM orders o
INNER JOIN order_items oi
ON o.order_id = oi.order_id
INNER JOIN products p
ON oi.product_id = p.product_id;


-- Q22. Difference between LEFT JOIN and RIGHT JOIN

-- LEFT JOIN:
-- Returns all rows from left table and matching rows
-- from right table. Non-matching rows show NULL.

SELECT 
    c.customer_id,
    c.first_name,
    o.order_id
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;


-- RIGHT JOIN:
-- Returns all rows from right table and matching rows
-- from left table.

SELECT 
    c.customer_id,
    c.first_name,
    o.order_id
FROM customers c
RIGHT JOIN orders o
ON c.customer_id = o.customer_id;


-- Explanation:
-- LEFT JOIN keeps all customers
-- RIGHT JOIN keeps all orders

-- FULL OUTER JOIN:
-- Returns all records from both tables.
-- Use when you want all customers and all orders,
-- whether matched or unmatched.



-- Q23. Foreign Key Relationships

-- 1. orders.customer_id → customers.customer_id
-- 2. order_items.order_id → orders.order_id
-- 3. order_items.product_id → products.product_id


-- Checking foreign keys using table description

DESCRIBE orders;
DESCRIBE order_items;


-- Example: Trying invalid foreign key insertion

INSERT INTO orders VALUES
(1011, 999, '2024-08-30', 'Pending', 1500.00);

-- Expected Error:
-- Cannot add or update a child row:
-- a foreign key constraint fails

-- Reason:
-- customer_id = 999 does not exist in customers table

