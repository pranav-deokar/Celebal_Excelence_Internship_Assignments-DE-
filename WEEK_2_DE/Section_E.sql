-- ============================================================
-- Celebal Technologies Summer Internship 2026
-- Week 2 Assignment
-- Section E: Advanced SQL & Data Validation
-- Dataset: Sample Superstore
-- Author: Pranav Deokar
-- ============================================================

-- Select database
USE shopease_db;


-- Q24. Classify products into price tiers using CASE
SELECT 
    product_name,
    unit_price,

    CASE
        WHEN unit_price < 1000 THEN 'Budget'
        WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
        WHEN unit_price > 3000 THEN 'Premium'
    END AS price_tier

FROM products;

-- Q25. Count Delivered vs Not Delivered orders
-- Using CASE inside aggregate function
SELECT 
    SUM(
        CASE 
            WHEN status = 'Delivered' THEN 1
            ELSE 0
        END
    ) AS delivered_orders,

    SUM(
        CASE 
            WHEN status != 'Delivered' THEN 1
            ELSE 0
        END
    ) AS not_delivered_orders

FROM orders;

-- Q26. ACID Properties Explanation

-- A = Atomicity
-- Means: Either all operations complete or none.
-- Example:
-- In bank transfer:
-- Money deducted from Account A and added to Account B.
-- If credit fails, debit also rolls back.

-- C = Consistency
-- Means: Database remains valid before and after transaction.
-- Example:
-- Total money before and after transfer remains same.

-- I = Isolation
-- Means: Multiple transactions do not interfere.
-- Example:
-- Two people transferring money at same time
-- should not affect each other's transactions.

-- D = Durability
-- Means: Once committed, data is permanently saved.
-- Example:
-- Even if system crashes after transfer,
-- committed transaction remains stored.


-- Q27. Transaction Example
-- Insert order, order items, update stock atomically

START TRANSACTION;

-- Step 1: Insert new order

INSERT INTO orders VALUES
(1011, 102, CURDATE(), 'Pending', 1598.00);


-- Step 2: Insert order items

INSERT INTO order_items VALUES
(5016, 1011, 202, 1, 799.00, 0),
(5017, 1011, 208, 1, 799.00, 0);

-- Step 3: Update stock quantities

UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 202;

UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 208;


-- Step 4: Commit transaction if successful

COMMIT;

-- If any query fails, run:

ROLLBACK;

-- Explanation:
-- Transaction ensures all steps execute together.
-- If any step fails:
-- Entire transaction is undone.
-- This maintains data consistency.


