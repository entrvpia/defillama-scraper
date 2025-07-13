import sqlite3
import pandas as pd

conn = sqlite3.connect('defillama_data.db')
df = pd.read_sql_query("SELECT * FROM defillama_metrics ORDER BY timestamp DESC", conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])
conn.close()
print(df.head())