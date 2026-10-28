# Olist E-commerce Sales Analytics

End-to-end analysis of 100K orders from a Brazilian online marketplace using SQL and Power BI, built to answer: where does revenue come from, and why are customers unhappy?

## Business Problem
An e-commerce marketplace wants to understand its revenue drivers and customer experience. This project answers five questions:
1. How do revenue and orders trend by month?
2. Which product categories and states drive revenue?
3. How many customers buy again?
4. How often are deliveries late?
5. Does late delivery lower review scores?

## Dataset
- Source: [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- About 100K orders (2016 to 2018) across 9 related tables
- Currency: Brazilian Real (BRL)
- The CSVs are not included in this repo. Download them and place them in `data/`.

## Approach
1. Loaded the 9 CSVs into SQLite (`load_data.py`)
2. Ran data quality checks (duplicates, nulls, order status)
3. Wrote SQL queries for KPIs, trends, categories, states, repeat customers and delivery delays
4. Exported result tables and built a Power BI dashboard

## KPIs
Revenue, Orders, Average Order Value, Repeat Customer %, Late Delivery %, Average Review Score

## Key Findings
_To be added after the analysis._

## Dashboard
_Screenshots to be added._
**[View the live dashboard](https://jay-aviral.github.io/olist-sales-analytics/)**
## Recommendations
_To be added._
echo "=== 1. Files Git tracks (what is on GitHub) ==="
git ls-files

echo; echo "=== 2. Big files tracked (over 5 MB) ==="
git ls-files | xargs -I{} du -k "{}" 2>/dev/null | awk '$1>5000'
echo "(blank = good)"

echo; echo "=== 3. Data/db tracked by mistake? ==="
git ls-files | grep -E "\.csv$|\.db$|\.sqlite|^data/" || echo "None (good)"

echo; echo "=== 4. Secrets tracked? ==="
git ls-files | grep -iE "kaggle\.json|\.env|token|secret|\.pem|\.key" || echo "None (good)"

echo; echo "=== 5. Secrets inside tracked files? ==="
git grep -n -iE "KAGGLE_KEY|api[_-]?key|password|token=" -- . ':!README.md' || echo "None (good)"

echo; echo "=== 6. Ignored (local only) ==="
git status --ignored -s | grep '^!!'

echo; echo "=== 7. Uncommitted changes ==="
git status -sb

echo; echo "=== 8. .gitignore ==="
cat .gitignore | grep -vE "^#|^$" | tail -10
## Limitations
_To be added._

## How to Run
```bash
pip install pandas
# download the 9 CSVs from Kaggle into data/
python load_data.py
# run the queries in sql/ or open 01_sql_checks.ipynb
```

## Tech Stack
SQL (SQLite), Python (Pandas), Power BI
