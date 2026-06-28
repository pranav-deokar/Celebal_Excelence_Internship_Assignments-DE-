-- ============================================================
-- Celebal Technologies Summer Internship 2026
-- Week 2 Assignment
-- Section C: Aggregation Queries
-- Dataset: Sample Superstore
-- Author: Pranav Deokar
-- ============================================================


-- Select database
USE shopease_db;

-- Q13. Count total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;


-- Q14. Total revenue from all Delivered orders
SELECT SUM(total_amount) AS total_delivered_revenue
FROM orders
WHERE status = 'Delivered';


-- Q15. Average product price in each category
SELECT 
    category,
    AVG(unit_price) AS average_price
FROM products
GROUP BY category;

-- Q16. For each order status:
-- Find count of orders and total revenue
-- Sort by total revenue (highest first)

SELECT 
    status,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC;

-- Q17. Find most expensive and cheapest product in each category

SELECT 
    category,
    MAX(unit_price) AS highest_price,
    MIN(unit_price) AS lowest_price
FROM products
GROUP BY category;

-- Q18. Categories where average unit_price > 2000
-- Using HAVING clause
SELECT 
    category,
    AVG(unit_price) AS average_price
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;

