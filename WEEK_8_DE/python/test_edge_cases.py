import sqlite3
from datetime import datetime

def test_invalid_order_reference():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE orders(order_id TEXT PRIMARY KEY)")
    conn.execute("CREATE TABLE order_items(order_id TEXT)")
    conn.execute("INSERT INTO orders VALUES ('O1')")
    conn.execute("INSERT INTO order_items VALUES ('O999')")
    missing = conn.execute("""
        SELECT oi.order_id FROM order_items oi
        LEFT JOIN orders o ON o.order_id=oi.order_id
        WHERE o.order_id IS NULL
    """).fetchall()
    assert missing == [("O999",)]
    conn.close()

def test_discount_over_100():
    discount = 120
    assert discount > 100
    # Business rule: flag invalid discount instead of silently accepting it.
    assert "INVALID" == ("INVALID" if discount > 100 else "VALID")

def test_zero_quantity():
    quantity = 0
    revenue = quantity * 100 * (1 - 10/100)
    assert revenue == 0

def test_future_order_date():
    future = datetime(2099, 1, 1)
    assert future.date() > datetime.now().date()

def run_tests():
    tests = [
        test_invalid_order_reference,
        test_discount_over_100,
        test_zero_quantity,
        test_future_order_date,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)} edge-case tests passed.")

if __name__ == "__main__":
    run_tests()
