-- ============================================================
-- Celebal Technologies Summer Internship 2026
-- Week 2 Assignment
-- Section B - Filtering & Optimization (WHERE, Indexes)
-- Dataset : Sample Superstore
-- Author : Pranav Deokar
-- ============================================================

-- Select database
USE shopease_db;


-- Q7. Retrieve all orders with status = 'Delivered'
SELECT *
FROM orders
WHERE status = 'Delivered';



-- Q8. Find all Electronics products with price > 2000
SELECT *
FROM products
WHERE category = 'Electronics'
AND unit_price > 2000;


-- Q9. Customers joined in 2024 and belong to Maharashtra
SELECT *
FROM customers
WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31'
AND state = 'Maharashtra';

-- Q10. Orders placed between 2024-08-10 and 2024-08-25
-- Excluding cancelled orders
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
AND status != 'Cancelled';


-- Q11. Index Explanation: idx_orders_date
-- Existing Index:
-- CREATE INDEX idx_orders_date ON orders(order_date);

-- Explanation:
-- This index speeds up searching, filtering, and sorting
-- based on order_date.

-- Without index:
-- MySQL scans all rows (Full Table Scan)

-- With index:
-- MySQL directly jumps to matching rows
-- (Faster for large datasets)

-- Sample query using this index:
SELECT *
FROM orders
WHERE order_date = '2024-08-15';

-- This query benefits from idx_orders_date


-- Q12. Index Usage on YEAR(join_date)

-- Query:

SELECT *
FROM customers
WHERE YEAR(join_date) = 2024;

-- Explanation:
-- This is NOT index-friendly because YEAR() applies a function
-- on the column, so MySQL cannot directly use the index.

-- This causes Full Table Scan.

-- Index-friendly (SARGable) query:

SELECT *
FROM customers
WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Why better?
-- It directly compares raw column values
-- allowing index usage for faster filtering.

