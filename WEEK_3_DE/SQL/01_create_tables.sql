-- Week 3 Assignment
-- Create Database and Tables

CREATE DATABASE IF NOT EXISTS celebal_week3;

USE celebal_week3;

-- Raw table for importing CSV

CREATE TABLE superstore_raw (
    row_id VARCHAR(20),
    order_id VARCHAR(30),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(30),
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    region VARCHAR(50),
    product_id VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name VARCHAR(255),
    sales VARCHAR(30),
    quantity VARCHAR(20),
    discount VARCHAR(20),
    profit VARCHAR(30)
);

-- Customers table

CREATE TABLE customers (
    customer_id VARCHAR(30),
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INT,
    region VARCHAR(50)
);

-- Products table

CREATE TABLE products (
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(50),
    sub_category VARCHAR(50)
);

-- Orders table

CREATE TABLE orders (
    row_id INT,
    order_id VARCHAR(30),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(30),
    product_id VARCHAR(50),
    sales DECIMAL(12,4),
    quantity INT,
    discount DECIMAL(6,4),
    profit DECIMAL(12,4)
);