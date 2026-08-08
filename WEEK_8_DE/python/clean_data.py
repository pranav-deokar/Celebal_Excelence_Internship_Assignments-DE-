import csv
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "cleaned"
REPORTS = ROOT / "reports"
CLEAN.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

issues = []

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def parse_order_date(value):
    value = (value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
    return None

def clean_orders(rows):
    cleaned = []
    for row in rows:
        order_id = row["order_id"]
        customer_id = (row["customer_id"] or "").strip()
        order_date = row["order_date"]

        if not customer_id:
            issues.append(["orders.csv", order_id, "Missing customer_id", "Replaced with UNKNOWN"])
            customer_id = "UNKNOWN"

        parsed = parse_order_date(order_date)
        if parsed is None:
            issues.append(["orders.csv", order_id, "Invalid order_date", "Set to blank"])
            parsed = ""
        elif parsed != order_date:
            issues.append(["orders.csv", order_id, "Wrong date format", "Converted to YYYY-MM-DD HH:MM:SS"])

        cleaned.append([
            order_id, customer_id, parsed,
            row["status"].strip().upper(), row["region_code"].strip().upper()
        ])
    return cleaned

def clean_products(rows):
    cleaned = []
    for row in rows:
        original = row["product_name"]
        normalized = " ".join(original.strip().split()).title()
        if normalized != original:
            issues.append(["products.csv", row["product_id"], "Messy product_name",
                           "Trimmed spaces and applied title case"])
        cleaned.append([
            row["product_id"], normalized, row["category"].strip().title(),
            row["subcategory"].strip().title(), row["cost_price"]
        ])
    return cleaned

def validate_emails(rows):
    invalid_ids = []
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    for row in rows:
        if not pattern.fullmatch(row["email"] or ""):
            invalid_ids.append(row["customer_id"])
            issues.append(["customers.csv", row["customer_id"], "Invalid email",
                           "Reported; original value retained"])
    return invalid_ids

def check_referential_integrity(order_rows, item_rows):
    valid_order_ids = {row["order_id"] for row in order_rows}
    invalid_items = []
    for row in item_rows:
        if row["order_id"] not in valid_order_ids:
            invalid_items.append(row)
            issues.append(["order_items.csv", row["item_id"], "Non-existent order_id", "Reported"])
    return invalid_items

def main():
    orders = read_csv(RAW / "orders.csv")
    items = read_csv(RAW / "order_items.csv")
    products = read_csv(RAW / "products.csv")
    customers = read_csv(RAW / "customers.csv")

    cleaned_orders = clean_orders(orders)
    cleaned_products = clean_products(products)
    invalid_emails = validate_emails(customers)
    bad_refs = check_referential_integrity(orders, items)

    write_csv(CLEAN / "orders_cleaned.csv",
              ["order_id","customer_id","order_date","status","region_code"], cleaned_orders)
    write_csv(CLEAN / "order_items_cleaned.csv",
              ["item_id","order_id","product_id","quantity","unit_price","discount_percent"],
              [[r["item_id"], r["order_id"], r["product_id"], r["quantity"], r["unit_price"], r["discount_percent"]]
               for r in items])
    write_csv(CLEAN / "products_cleaned.csv",
              ["product_id","product_name","category","subcategory","cost_price"], cleaned_products)
    write_csv(CLEAN / "customers_cleaned.csv",
              ["customer_id","customer_name","email","registration_date","customer_type"],
              [[r["customer_id"],r["customer_name"],r["email"],r["registration_date"],r["customer_type"]]
               for r in customers])

    write_csv(REPORTS / "cleaning_issue_report.csv",
              ["file","record_id","issue","action"], issues)

    write_csv(REPORTS / "validation_report.csv",
              ["check","count","details"], [
                  ["Invalid emails", len(invalid_emails), ", ".join(invalid_emails)],
                  ["Invalid order references", len(bad_refs),
                   ", ".join(r["item_id"] for r in bad_refs) if bad_refs else "None"]
              ])

    print("Data cleaning complete.")
    print(f"Cleaning issues recorded: {len(issues)}")
    print(f"Invalid emails found: {len(invalid_emails)}")
    print(f"Invalid order references found: {len(bad_refs)}")

if __name__ == "__main__":
    main()
