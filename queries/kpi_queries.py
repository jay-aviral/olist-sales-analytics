import sqlite3, pandas as pd
conn = sqlite3.connect("olist.db")
def q(sql): return pd.read_sql(sql, conn)

print("=== KPIs (delivered orders) ===")
print(q("""
SELECT COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(p.payment_value), 2) AS revenue,
       ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
"""))

print("=== Monthly revenue ===")
print(q("""
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY 1
"""))
