import sqlite3
import pandas as pd

conn = sqlite3.connect("data/clientes.db")

for nombre, query in [
    ("Por producto", "SELECT producto, COUNT(*) n, ROUND(AVG(saldo),2) saldo_prom FROM clientes GROUP BY producto"),
    ("Por ciudad", "SELECT ciudad, COUNT(*) n FROM clientes GROUP BY ciudad ORDER BY n DESC"),
]:
    print(f"\n{nombre}:")
    print(pd.read_sql(query, conn))

conn.close()