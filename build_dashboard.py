import sqlite3, pandas as pd, plotly.express as px

conn = sqlite3.connect("olist.db")
q = lambda sql: pd.read_sql(sql, conn)

kpi = q("""
SELECT COUNT(DISTINCT o.order_id) AS orders,
       SUM(p.payment_value) AS revenue
FROM orders o JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'""").iloc[0]
aov = kpi.revenue / kpi.orders

monthly = q("""
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       SUM(p.payment_value) AS revenue
FROM orders o JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY 1""")

cats = q("""
SELECT COALESCE(t.product_category_name_english, p.product_category_name) AS category,
       SUM(i.price) AS revenue
FROM orders o
JOIN order_items i ON o.order_id = i.order_id
JOIN products p ON i.product_id = p.product_id
LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY 2 DESC LIMIT 10""")

states = q("""
SELECT c.customer_state AS state, SUM(pay.payment_value) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments pay ON o.order_id = pay.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY 2 DESC LIMIT 10""")

rev = q("""
SELECT CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
            THEN 'Late' ELSE 'On time' END AS delivery,
       ROUND(AVG(r.review_score), 2) AS avg_review
FROM orders o JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1""")

figs = [
    px.line(monthly, x="month", y="revenue", title="Monthly revenue (BRL)"),
    px.bar(cats, x="revenue", y="category", orientation="h", title="Top 10 categories by item revenue"),
    px.bar(states, x="state", y="revenue", title="Top 10 states by revenue (BRL)"),
    px.bar(rev, x="delivery", y="avg_review", text="avg_review", title="Average review score: late vs on-time"),
]
figs[1].update_yaxes(autorange="reversed")

html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Olist Sales Analytics</title>
<style>body{{font-family:sans-serif;max-width:1000px;margin:auto;padding:16px}}
.k{{display:flex;gap:16px}}.k div{{flex:1;background:#f3f4f6;padding:16px;border-radius:8px}}
.k b{{font-size:24px;display:block}}</style></head><body>
<h1>Olist E-commerce Sales Dashboard</h1>
<p>Delivered orders only. Revenue = payment value (includes freight), in BRL.</p>
<div class="k"><div>Orders<b>{int(kpi.orders):,}</b></div>
<div>Revenue<b>{kpi.revenue:,.0f}</b></div>
<div>Avg order value<b>{aov:,.2f}</b></div></div>
{''.join(f.to_html(full_html=False, include_plotlyjs='cdn' if i == 0 else False) for i, f in enumerate(figs))}
</body></html>"""

open("docs/index.html", "w").write(html)
print("Saved docs/index.html")
