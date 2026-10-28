import sqlite3, pandas as pd
conn = sqlite3.connect("olist.db")
print(pd.read_sql("""
SELECT c.customer_state AS state,
       COUNT(*) AS orders,
       ROUND(100.0 * SUM(o.order_delivered_customer_date > o.order_estimated_delivery_date) / COUNT(*), 1) AS late_pct
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1 HAVING COUNT(*) > 500
ORDER BY late_pct DESC LIMIT 8
""", conn).to_string(index=False))
