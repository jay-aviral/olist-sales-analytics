import sqlite3, pandas as pd
conn = sqlite3.connect("olist.db")
def q(sql): return pd.read_sql(sql, conn).to_string(index=False)

print("=== Top 10 categories by item revenue (delivered) ===")
print(q("""
SELECT COALESCE(t.product_category_name_english, p.product_category_name) AS category,
       COUNT(*) AS items,
       ROUND(SUM(i.price), 2) AS revenue
FROM orders o
JOIN order_items i ON o.order_id = i.order_id
JOIN products p ON i.product_id = p.product_id
LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY 3 DESC LIMIT 10
"""))

print("\n=== Top 10 states by revenue (delivered) ===")
print(q("""
SELECT c.customer_state AS state,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(pay.payment_value), 2) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments pay ON o.order_id = pay.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY 3 DESC LIMIT 10
"""))

print("\n=== Repeat customers ===")
print(q("""
SELECT COUNT(*) AS customers,
       SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END) AS repeat_customers,
       ROUND(100.0 * SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_pct
FROM (SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS n
      FROM orders o JOIN customers c ON o.customer_id = c.customer_id
      WHERE o.order_status = 'delivered'
      GROUP BY 1)
"""))

print("\n=== Late delivery vs review score ===")
print(q("""
SELECT CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
            THEN 'late' ELSE 'on_time' END AS delivery,
       COUNT(*) AS orders,
       ROUND(AVG(r.review_score), 2) AS avg_review
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1
"""))
