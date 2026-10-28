import sqlite3, pandas as pd
conn = sqlite3.connect("olist.db")
def q(sql): return pd.read_sql(sql, conn)

print(q("SELECT name FROM sqlite_master WHERE type='table'"))
print(q("SELECT COUNT(*) AS orders FROM orders"))
print(q("SELECT order_status, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC"))
print(q("SELECT MIN(order_purchase_timestamp) AS first_order, MAX(order_purchase_timestamp) AS last_order FROM orders"))
print(q("SELECT COUNT(*) AS dup_order_ids FROM (SELECT order_id FROM orders GROUP BY 1 HAVING COUNT(*) > 1)"))
print(q("SELECT COUNT(*) AS null_delivery_dates FROM orders WHERE order_delivered_customer_date IS NULL"))
