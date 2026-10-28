import sqlite3, pandas as pd
from pathlib import Path

conn = sqlite3.connect("olist.db")
for f in Path("data").glob("*.csv"):
    name = f.stem.replace("olist_", "").replace("_dataset", "")
    pd.read_csv(f).to_sql(name, conn, if_exists="replace", index=False)
    print("loaded", name)
conn.close()
