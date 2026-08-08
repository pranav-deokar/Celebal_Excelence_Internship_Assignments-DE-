import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "cleaned"
DB = ROOT / "ecommerce.db"

def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        customer_name TEXT NOT NULL,
        email TEXT,
        registration_date TEXT,
        customer_type TEXT
    );
    CREATE TABLE products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        subcategory TEXT,
        cost_price REAL
    );
    CREATE TABLE orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_date TEXT,
        status TEXT,
        region_code TEXT
    );
    CREATE TABLE order_items (
        item_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        quantity INTEGER,
        unit_price REAL,
        discount_percent REAL
    );
    """)

    customers = read(CLEAN/"customers_cleaned.csv")
    products = read(CLEAN/"products_cleaned.csv")
    orders = read(CLEAN/"orders_cleaned.csv")
    items = read(CLEAN/"order_items_cleaned.csv")

    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)",
                    [(r["customer_id"],r["customer_name"],r["email"],r["registration_date"],r["customer_type"])
                     for r in customers])
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)",
                    [(r["product_id"],r["product_name"],r["category"],r["subcategory"],float(r["cost_price"]))
                     for r in products])
    cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?)",
                    [(r["order_id"],r["customer_id"],r["order_date"],r["status"],r["region_code"])
                     for r in orders])
    cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?)",
                    [(r["item_id"],r["order_id"],r["product_id"],int(r["quantity"]),
                      float(r["unit_price"]),float(r["discount_percent"])) for r in items])

    conn.commit()
    print(f"SQLite database created: {DB}")
    for table in ("customers","products","orders","order_items"):
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count} rows")
    conn.close()

if __name__ == "__main__":
    main()
