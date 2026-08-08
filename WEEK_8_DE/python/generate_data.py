import csv
import random
from datetime import datetime, timedelta, date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

random.seed(42)

CATEGORIES = {
    "Electronics": ["Mobiles", "Laptops", "Audio", "Accessories"],
    "Clothing": ["Men", "Women", "Footwear", "Accessories"],
    "Home": ["Kitchen", "Furniture", "Decor", "Appliances"],
    "Books": ["Fiction", "Non-Fiction", "Education", "Technology"],
}
PRODUCT_TEMPLATES = {
    "Electronics": ["Wireless Headphones", "Smartphone", "Laptop", "Bluetooth Speaker", "USB-C Cable",
                    "Mechanical Keyboard", "Smart Watch", "Power Bank", "Webcam", "Mouse"],
    "Clothing": ["Cotton Shirt", "Denim Jeans", "Running Shoes", "Hoodie", "Jacket",
                 "Casual Trousers", "Sneakers", "Backpack", "Socks", "Cap"],
    "Home": ["Coffee Maker", "Table Lamp", "Office Chair", "Bedsheet Set", "Storage Box",
             "Water Bottle", "Cookware Set", "Wall Clock", "Cushion Set", "Vacuum Cleaner"],
    "Books": ["Python Programming", "Data Engineering", "Machine Learning Basics", "SQL Handbook",
              "Cloud Computing", "Artificial Intelligence", "Clean Code", "Statistics Guide",
              "Web Development", "Database Systems"],
}

def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_customers(n=650):
    rows = []
    first_names = ["Aarav","Vivaan","Aditya","Arjun","Rohan","Rahul","Karan","Pranav","Ishaan","Kabir",
                   "Ananya","Diya","Isha","Aditi","Sneha","Meera","Pooja","Riya","Nisha","Kavya"]
    last_names = ["Sharma","Patil","Deshmukh","Kulkarni","Joshi","Singh","Verma","Pawar","More","Jadhav"]
    for i in range(1, n + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        reg_date = date(2025, 1, 1) + timedelta(days=random.randint(0, 500))
        email = f"{first.lower()}.{last.lower()}{i}@example.com"
        if i % 50 == 0:  # 2%
            email = f"{first.lower()}.{last.lower()}{i}example.com"
        rows.append([f"C{i:04d}", f"{first} {last}", email, reg_date.isoformat(),
                     random.choice(["REGULAR", "PREMIUM", "VIP"])])
    return rows

def generate_products():
    rows = []
    pid = 1
    for category, names in PRODUCT_TEMPLATES.items():
        for name in names:
            for _ in range(2):
                subcategory = random.choice(CATEGORIES[category])
                cost = round(random.uniform(150, 35000 if category == "Electronics" else 10000), 2)
                product_name = name
                if pid % 11 == 0:
                    product_name = f"  {name.lower()}  "
                elif pid % 13 == 0:
                    product_name = name.upper()
                elif pid % 17 == 0:
                    product_name = f" {name} "
                rows.append([f"P{pid:04d}", product_name, category, subcategory, cost])
                pid += 1
    return rows

def generate_orders(customers, n=1200):
    rows = []
    start = datetime(2025, 1, 1)
    end = datetime(2026, 8, 5)
    days = (end.date() - start.date()).days
    statuses = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
    regions = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]

    for i in range(1, n + 1):
        dt = start + timedelta(days=random.randint(0, days),
                               hours=random.randint(8, 21),
                               minutes=random.randint(0, 59),
                               seconds=random.randint(0, 59))
        customer_id = "" if i % 20 == 0 else random.choice(customers)[0]  # 5%
        status = random.choices(statuses, weights=[18, 17, 43, 8, 14], k=1)[0]
        region = random.choice(regions)
        if i % 37 == 0:
            order_date = dt.strftime("%d-%m-%Y %H:%M:%S")
        else:
            order_date = dt.strftime("%Y-%m-%d %H:%M:%S")
        rows.append([f"O{i:05d}", customer_id, order_date, status, region])
    return rows

def generate_order_items(orders, products):
    rows = []
    item_id = 1
    product_ids = [p[0] for p in products]
    for order in orders:
        order_id = order[0]
        for _ in range(random.randint(1, 4)):
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 5)
            if item_id % 33 == 0:  # approximately 3%
                quantity = -random.randint(1, 3)
            unit_price = round(random.uniform(250, 50000), 2)
            discount = round(random.choice([0, 0, 5, 10, 15, 20, 25, 30]), 2)
            rows.append([f"OI{item_id:06d}", order_id, product_id, quantity, unit_price, discount])
            item_id += 1
    return rows

def main():
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)

    write_csv(RAW / "orders.csv",
              ["order_id","customer_id","order_date","status","region_code"], orders)
    write_csv(RAW / "order_items.csv",
              ["item_id","order_id","product_id","quantity","unit_price","discount_percent"], order_items)
    write_csv(RAW / "products.csv",
              ["product_id","product_name","category","subcategory","cost_price"], products)
    write_csv(RAW / "customers.csv",
              ["customer_id","customer_name","email","registration_date","customer_type"], customers)

    print("Data generation complete.")
    print(f"orders.csv: {len(orders)} rows")
    print(f"order_items.csv: {len(order_items)} rows")
    print(f"products.csv: {len(products)} rows")
    print(f"customers.csv: {len(customers)} rows")

if __name__ == "__main__":
    main()
