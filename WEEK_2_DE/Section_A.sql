-- ============================================================
-- Celebal Technologies Summer Internship 2026
-- Week 2 Assignment
-- Section A - SQL Basics (SELECT, Constraints, Primary Keys)
-- Dataset : Sample Superstore
-- Author : Pranav Deokar
-- ============================================================


-- Select the database
USE shopease_db;

-- Q1. Display all columns and rows from customers table
SELECT * 
FROM customers;

-- Q2. Retrieve only first_name, last_name, and city of all customers
SELECT 
    first_name,
    last_name,
    city
FROM customers;

-- Q3. List all unique categories in products table
SELECT DISTINCT category
FROM products;

-- Q4. Identify Primary Key of each table
-- Using DESCRIBE command to check schema structure
DESCRIBE customers;
DESCRIBE products;
DESCRIBE orders;
DESCRIBE order_items;

-- Primary Keys:
-- customers   -> customer_id
-- products    -> product_id
-- orders      -> order_id
-- order_items -> item_id

-- Explanation:
-- Primary Key must be UNIQUE and NOT NULL
-- It uniquely identifies each record in a table.

-- Q4 (Practical Example)
-- Trying duplicate Primary Key insertion
INSERT INTO customers VALUES
(101, 'Test', 'User', 'test@email.com', 'Pune', 'Maharashtra', '2024-01-01', TRUE);
--  Error:
-- Duplicate entry '101' for key 'PRIMARY'

-- Q5. Constraints on email column
-- email has UNIQUE and NOT NULL constraints
-- Trying duplicate email insertion
INSERT INTO customers VALUES
(109, 'Rahul', 'Patil', 'aarav.s@email.com', 'Nagpur', 'Maharashtra', '2024-09-01', FALSE);

-- Expected Error:
-- Duplicate entry 'aarav.s@email.com' for key 'email'

-- Q6. Insert product with negative unit_price
-- Testing CHECK constraint
INSERT INTO products VALUES
(209, 'Test Product', 'Electronics', 'TestBrand', -50, 100);

-- Expected Error:
-- Check constraint 'unit_price > 0' is violated


-- Valid Insert Example (Correct Data)
INSERT INTO products VALUES
(209, 'Test Product', 'Electronics', 'TestBrand', 500, 100);

