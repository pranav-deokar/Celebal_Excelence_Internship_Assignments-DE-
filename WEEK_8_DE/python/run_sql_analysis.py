import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "ecommerce.db"
OUT = ROOT / "reports" / "sql_results"
OUT.mkdir(parents=True, exist_ok=True)

REV = "(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0))"

QUERIES = {
"01_total_revenue_per_category": f"""
SELECT p.category, ROUND(SUM({REV}), 2) AS total_revenue
FROM order_items oi JOIN products p ON p.product_id=oi.product_id
GROUP BY p.category ORDER BY total_revenue DESC;
""",
"02_top_10_customers": f"""
SELECT o.customer_id, ROUND(SUM({REV}),2) AS total_order_value
FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
WHERE o.customer_id <> 'UNKNOWN'
GROUP BY o.customer_id ORDER BY total_order_value DESC LIMIT 10;
""",
"03_monthly_order_count_last_12_months": """
WITH max_date AS (SELECT MAX(date(order_date)) AS d FROM orders)
SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS order_count
FROM orders, max_date
WHERE date(order_date) >= date(max_date.d, '-11 months')
GROUP BY month ORDER BY month;
""",
"04_customers_never_had_delivered_item": """
SELECT DISTINCT o.customer_id
FROM orders o
WHERE o.customer_id <> 'UNKNOWN'
AND EXISTS (SELECT 1 FROM order_items oi WHERE oi.order_id=o.order_id)
AND NOT EXISTS (
    SELECT 1 FROM orders od
    WHERE od.customer_id=o.customer_id AND od.status='DELIVERED'
);
""",
"05_products_more_returns_than_purchases": """
WITH product_flow AS (
    SELECT p.product_id, p.product_name,
           SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS purchases,
           SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS returns
    FROM products p JOIN order_items oi ON oi.product_id=p.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT product_id, product_name, purchases, returns
FROM product_flow WHERE returns > purchases
ORDER BY returns DESC;
""",
"06_return_rate_per_category": """
SELECT p.category,
       SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS returned_items,
       SUM(ABS(oi.quantity)) AS total_items,
       ROUND(100.0 * SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END)
             / NULLIF(SUM(ABS(oi.quantity)),0), 2) AS return_rate_percent
FROM order_items oi JOIN products p ON p.product_id=oi.product_id
GROUP BY p.category ORDER BY return_rate_percent DESC;
""",
"07_running_totals": f"""
WITH daily AS (
    SELECT o.region_code, date(o.order_date) AS order_date,
           SUM({REV}) AS daily_revenue
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    GROUP BY o.region_code, date(o.order_date)
)
SELECT region_code, order_date, ROUND(daily_revenue,2) AS daily_revenue,
       ROUND(SUM(daily_revenue) OVER (
           PARTITION BY region_code ORDER BY order_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_total
FROM daily ORDER BY region_code, order_date;
""",
"08_dense_rank": f"""
WITH product_revenue AS (
    SELECT p.category, p.product_name, SUM({REV}) AS total_revenue
    FROM products p JOIN order_items oi ON oi.product_id=p.product_id
    GROUP BY p.product_id, p.category, p.product_name
)
SELECT category, product_name, ROUND(total_revenue,2) AS total_revenue,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue ORDER BY category, rank_in_category, product_name;
""",
"09_lag_lead_analysis": """
WITH ordered AS (
    SELECT customer_id, order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date,
           LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_order_date
    FROM orders WHERE customer_id <> 'UNKNOWN'
),
gaps AS (
    SELECT customer_id, order_date, previous_order_date, next_order_date,
           CASE WHEN previous_order_date IS NULL THEN NULL
                ELSE ROUND(julianday(order_date)-julianday(previous_order_date),2) END AS days_gap
    FROM ordered
),
risk AS (
    SELECT customer_id, AVG(days_gap) AS avg_gap
    FROM gaps WHERE days_gap IS NOT NULL GROUP BY customer_id
)
SELECT g.customer_id, g.order_date, g.previous_order_date, g.days_gap,
       CASE WHEN r.avg_gap > 30 THEN 'At Risk' ELSE 'Active' END AS customer_status
FROM gaps g JOIN risk r ON r.customer_id=g.customer_id
ORDER BY g.customer_id, g.order_date;
""",
"10_cte_multiple_levels": f"""
WITH monthly_customer AS (
    SELECT o.customer_id, strftime('%Y-%m',o.order_date) AS month,
           SUM({REV}) AS monthly_revenue
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    WHERE o.customer_id <> 'UNKNOWN'
    GROUP BY o.customer_id, month
),
segmented AS (
    SELECT customer_id, month, monthly_revenue,
           CASE WHEN monthly_revenue > 10000 THEN 'High'
                WHEN monthly_revenue >= 5000 THEN 'Medium'
                ELSE 'Low' END AS value_category
    FROM monthly_customer
)
SELECT month, value_category, COUNT(*) AS customer_count
FROM segmented GROUP BY month, value_category
ORDER BY month, CASE value_category WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END;
""",
"11_ntile_segmentation": f"""
WITH lifetime AS (
    SELECT o.customer_id, SUM({REV}) AS total_value
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    WHERE o.customer_id <> 'UNKNOWN'
    GROUP BY o.customer_id
),
q AS (
    SELECT customer_id, total_value,
           NTILE(4) OVER (ORDER BY total_value DESC) AS quartile
    FROM lifetime
)
SELECT customer_id, ROUND(total_value,2) AS total_value, quartile,
       CASE quartile WHEN 1 THEN 'Platinum' WHEN 2 THEN 'Gold'
                    WHEN 3 THEN 'Silver' ELSE 'Bronze' END AS quartile_label
FROM q ORDER BY quartile, total_value DESC;
""",
"12_year_over_year": f"""
WITH monthly AS (
    SELECT CAST(strftime('%Y',o.order_date) AS INTEGER) AS year,
           CAST(strftime('%m',o.order_date) AS INTEGER) AS month,
           SUM({REV}) AS revenue
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    GROUP BY year, month
),
joined AS (
    SELECT m.year, m.month, m.revenue, p.revenue AS prev_year_revenue
    FROM monthly m
    LEFT JOIN monthly p ON p.year=m.year-1 AND p.month=m.month
)
SELECT year, month, ROUND(revenue,2) AS revenue,
       ROUND(prev_year_revenue,2) AS prev_year_revenue,
       CASE WHEN prev_year_revenue IS NULL OR prev_year_revenue=0 THEN NULL
            ELSE ROUND(100.0*(revenue-prev_year_revenue)/prev_year_revenue,2) END AS yoy_growth_percent
FROM joined ORDER BY year, month;
""",
"13_first_last_value_analysis": f"""
WITH purchased AS (
    SELECT o.customer_id, o.order_date, o.order_id, p.category,
           FIRST_VALUE(p.category) OVER (
               PARTITION BY o.customer_id ORDER BY o.order_date, o.order_id
               ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ) AS first_category,
           LAST_VALUE(p.category) OVER (
               PARTITION BY o.customer_id ORDER BY o.order_date, o.order_id
               ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ) AS last_category
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    JOIN products p ON p.product_id=oi.product_id
    WHERE o.customer_id <> 'UNKNOWN'
)
SELECT DISTINCT customer_id, first_category, last_category,
       CASE WHEN first_category <> last_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM purchased ORDER BY customer_id;
""",
"14_cumulative_distribution": f"""
WITH customer_revenue AS (
    SELECT o.customer_id, SUM({REV}) AS revenue
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    WHERE o.customer_id <> 'UNKNOWN'
    GROUP BY o.customer_id
),
ranked AS (
    SELECT customer_id, revenue,
           SUM(revenue) OVER (ORDER BY revenue DESC ROWS UNBOUNDED PRECEDING) AS cumulative_revenue,
           SUM(revenue) OVER () AS total_revenue
    FROM customer_revenue
)
SELECT customer_id, ROUND(revenue,2) AS revenue,
       ROUND(cumulative_revenue,2) AS cumulative_revenue,
       ROUND(100.0*cumulative_revenue/NULLIF(total_revenue,0),2) AS cumulative_percent
FROM ranked ORDER BY revenue DESC;
""",
"15_cohort_analysis": """
WITH customer_cohort AS (
    SELECT customer_id, strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
),
order_months AS (
    SELECT DISTINCT o.customer_id, strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o WHERE o.customer_id <> 'UNKNOWN'
),
cohort_orders AS (
    SELECT c.cohort_month, o.customer_id, o.order_month,
           (CAST(strftime('%Y',o.order_month||'-01') AS INTEGER) - CAST(strftime('%Y',c.cohort_month||'-01') AS INTEGER))*12
           + (CAST(strftime('%m',o.order_month||'-01') AS INTEGER) - CAST(strftime('%m',c.cohort_month||'-01') AS INTEGER)) AS month_number
    FROM customer_cohort c JOIN order_months o ON o.customer_id=c.customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM customer_cohort GROUP BY cohort_month
)
SELECT co.cohort_month, cs.cohort_customers,
       COUNT(DISTINCT CASE WHEN co.month_number=0 THEN co.customer_id END) AS month_0,
       COUNT(DISTINCT CASE WHEN co.month_number=1 THEN co.customer_id END) AS month_1,
       COUNT(DISTINCT CASE WHEN co.month_number=2 THEN co.customer_id END) AS month_2,
       COUNT(DISTINCT CASE WHEN co.month_number=3 THEN co.customer_id END) AS month_3,
       ROUND(100.0*COUNT(DISTINCT CASE WHEN co.month_number=0 THEN co.customer_id END)/cs.cohort_customers,2) AS retention_0_pct,
       ROUND(100.0*COUNT(DISTINCT CASE WHEN co.month_number=1 THEN co.customer_id END)/cs.cohort_customers,2) AS retention_1_pct,
       ROUND(100.0*COUNT(DISTINCT CASE WHEN co.month_number=2 THEN co.customer_id END)/cs.cohort_customers,2) AS retention_2_pct,
       ROUND(100.0*COUNT(DISTINCT CASE WHEN co.month_number=3 THEN co.customer_id END)/cs.cohort_customers,2) AS retention_3_pct
FROM cohort_orders co JOIN cohort_size cs ON cs.cohort_month=co.cohort_month
GROUP BY co.cohort_month, cs.cohort_customers ORDER BY co.cohort_month;
""",
"16_self_join_window_function": f"""
WITH customer_orders AS (
    SELECT o.customer_id, o.order_id, date(o.order_date) AS order_date,
           SUM({REV}) AS order_value
    FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
    WHERE o.customer_id <> 'UNKNOWN'
    GROUP BY o.customer_id, o.order_id, date(o.order_date)
),
sequenced AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
    FROM customer_orders
)
SELECT a.customer_id,
       a.order_id AS current_order_id,
       a.order_date AS current_order_date,
       ROUND(a.order_value,2) AS current_order_value,
       b.order_id AS previous_order_id,
       b.order_date AS previous_order_date,
       ROUND(b.order_value,2) AS previous_order_value,
       ROUND(a.order_value-COALESCE(b.order_value,0),2) AS value_change
FROM sequenced a
LEFT JOIN sequenced b
  ON b.customer_id=a.customer_id AND b.rn=a.rn-1
ORDER BY a.customer_id, a.rn;
"""
}

def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    errors = []

    for name, query in QUERIES.items():
        try:
            result = cur.execute(query)
            rows = result.fetchall()
            cols = [d[0] for d in result.description]
            write_csv(OUT / f"{name}.csv", cols, rows)
        except Exception as exc:
            errors.append((name, str(exc)))

    # Required Part 5 product-pair analysis.
    pair_query = """
    WITH order_products AS (
        SELECT DISTINCT order_id, product_id FROM order_items
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
    """
    rows = cur.execute(pair_query).fetchall()
    cols = [d[0] for d in cur.description]
    write_csv(ROOT/"reports"/"frequently_bought_together.csv", cols, rows)

    conn.close()

    if errors:
        print("SQL errors:")
        for name, error in errors:
            print(name, "->", error)
        raise SystemExit(1)

    print(f"Executed {len(QUERIES)} SQL analysis queries successfully.")
    print("Results saved in reports/sql_results/")
    print("Frequently-bought-together result saved in reports/frequently_bought_together.csv")

if __name__ == "__main__":
    main()
