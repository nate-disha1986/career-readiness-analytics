"""
Run SQL analysis queries and print results.
Author: Disha Nate
"""

import pandas as pd
import sqlite3
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "career_readiness.db"
SQL_FILE = PROJECT_ROOT / "sql" / "03_analysis_queries.sql"

print("=" * 70)
print("RUNNING SQL BUSINESS QUERIES")
print("=" * 70)

# Read SQL file
sql_text = SQL_FILE.read_text(encoding='utf-8')

# Split by query block
queries = re.split(r'-- =+\n-- QUERY (\d+):', sql_text)

# Connect
conn = sqlite3.connect(DB_PATH)

# Process each query
i = 1
while i < len(queries) - 1:
    query_num = queries[i]
    query_body = queries[i + 1]

    # Extract title (first line)
    lines = query_body.strip().split('\n')
    title = lines[0].replace('--', '').strip() if lines else f'Query {query_num}'

    # Extract SQL (everything after the comment header block)
    sql_start = query_body.find('SELECT')
    if sql_start == -1:
        i += 2
        continue
    sql = query_body[sql_start:].strip()

    # Run
    print(f"\n{'=' * 70}")
    print(f"QUERY {query_num}: {title}")
    print('=' * 70)
    try:
        result = pd.read_sql_query(sql, conn)
        print(result.to_string(index=False))
    except Exception as e:
        print(f"⚠ Error: {e}")

    i += 2

conn.close()
print("\n" + "=" * 70)
print("ALL QUERIES COMPLETE")
print("=" * 70)