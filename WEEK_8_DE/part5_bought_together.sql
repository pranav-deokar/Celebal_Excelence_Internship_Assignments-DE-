-- Frequently bought together; excludes same-product pairs and A-B/B-A duplicates.
WITH order_products AS (
    SELECT DISTINCT order_id, product_id
    FROM order_items
),
pairs AS (
    SELECT a.product_id AS product_a, b.product_id AS product_b, COUNT(*) AS times_bought_together
    FROM order_products a
    JOIN order_products b
      ON a.order_id=b.order_id AND a.product_id < b.product_id
    GROUP BY a.product_id, b.product_id
)
SELECT a.product_name AS product_a, b.product_name AS product_b, p.times_bought_together
FROM pairs p
JOIN products a ON a.product_id=p.product_a
JOIN products b ON b.product_id=p.product_b
ORDER BY p.times_bought_together DESC, product_a, product_b;
