USE celebal_week3;

-- 1. Top 5 customers based on total sales

SELECT
    customer_id,
    SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
ORDER BY total_sales DESC
LIMIT 5;

-- 2. Bottom 5 customers based on total sales

SELECT
    customer_id,
    SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
ORDER BY total_sales ASC
LIMIT 5;

-- 3. Customers who made only one order

SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) = 1;

-- 4. Customers whose total sales are above average

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM customer_sales
WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);

-- 5. Highest order value for each customer

SELECT
    customer_id,
    MAX(sales) AS highest_order_value
FROM orders
GROUP BY customer_id
ORDER BY highest_order_value DESC;