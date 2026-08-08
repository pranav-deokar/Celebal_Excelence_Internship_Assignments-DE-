#!/usr/bin/env python3
"""
Assignment 8 - Python + SQL Integration CLI
No external libraries are required.
"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "ecommerce.db"

def revenue_expression():
    return "(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0))"

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def get_period(start, end, report_type):
    if report_type == "daily":
        return start, end
    if report_type == "weekly":
        return start, end
    if report_type == "monthly":
        return start, end
    raise ValueError("Report type must be daily, weekly, or monthly.")

def summary(conn, start, end):
    rev = revenue_expression()
    row = conn.execute(f"""
        SELECT COUNT(DISTINCT o.order_id),
               COALESCE(SUM({rev}),0),
               COUNT(DISTINCT CASE WHEN o.customer_id <> 'UNKNOWN' THEN o.customer_id END)
        FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
        WHERE date(o.order_date) BETWEEN ? AND ?
    """, (start.isoformat(), end.isoformat())).fetchone()
    top3 = conn.execute(f"""
        SELECT p.product_name, ROUND(SUM({rev}),2) AS revenue
        FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
        JOIN products p ON p.product_id=oi.product_id
        WHERE date(o.order_date) BETWEEN ? AND ?
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC LIMIT 3
    """, (start.isoformat(), end.isoformat())).fetchall()
    return row, top3

def main():
    print("=== E-Commerce Order Analytics Report ===")
    report_type = input("Report type (daily/weekly/monthly): ").strip().lower()
    if report_type not in {"daily", "weekly", "monthly"}:
        raise SystemExit("Invalid report type.")
    start = parse_date(input("Start date (YYYY-MM-DD): ").strip())
    end = parse_date(input("End date (YYYY-MM-DD): ").strip())
    if end < start:
        raise SystemExit("End date must be on/after start date.")

    conn = sqlite3.connect(DB_PATH)
    current, top3 = summary(conn, start, end)
    days = (end - start).days + 1
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days-1)
    previous, _ = summary(conn, prev_start, prev_end)

    orders, revenue, customers = current
    prev_orders, prev_revenue, prev_customers = previous

    def pct_change(cur, prev):
        if prev == 0:
            return None
        return ((cur - prev) / abs(prev)) * 100

    print("\n--- Summary ---")
    print(f"Period: {start} to {end}")
    print(f"Report type: {report_type}")
    print(f"Total orders: {orders}")
    print(f"Revenue: {revenue:.2f}")
    print(f"Unique customers: {customers}")

    print("\n--- Top 3 Products ---")
    for name, value in top3:
        print(f"{name}: {value:.2f}")

    print("\n--- Previous Period Comparison ---")
    print(f"Previous period: {prev_start} to {prev_end}")
    print(f"Orders % change: {pct_change(orders, prev_orders):.2f}%" if pct_change(orders, prev_orders) is not None else "Orders % change: N/A")
    print(f"Revenue % change: {pct_change(revenue, prev_revenue):.2f}%" if pct_change(revenue, prev_revenue) is not None else "Revenue % change: N/A")
    print(f"Customers % change: {pct_change(customers, prev_customers):.2f}%" if pct_change(customers, prev_customers) is not None else "Customers % change: N/A")
    conn.close()

if __name__ == "__main__":
    main()
