import duckdb

conn = duckdb.connect(r'D:\SSD-files\Telugu LLM\Codes\parquet_converter\parquets\partial-index.duckdb')

result = conn.execute('SHOW TABLES').fetchall()

for row in result:
    print(row)
