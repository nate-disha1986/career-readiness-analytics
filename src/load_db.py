"""
Load enriched data into SQLite database.
Author: Disha Nate
"""

import pandas as pd
from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).parent.parent
ENRICHED_DATA = PROJECT_ROOT / "data" / "processed" / "responses_enriched.csv"
DB_PATH = PROJECT_ROOT / "data" / "processed" / "career_readiness.db"

print("=" * 70)
print("LOADING DATA INTO SQLITE")
print("=" * 70)

# Load enriched CSV
df = pd.read_csv(ENRICHED_DATA)
print(f"\nLoaded CSV: {df.shape[0]} rows × {df.shape[1]} columns")

# Keep only the columns we want in SQL
sql_cols = [
    'sr_no', 'timestamp', 'age_group', 'age_clean', 'gender', 'education',
    'career_goal_clarity', 'career_field', 'career_path',
    'confidence', 'understanding', 'important_skills',
    'skill_rating', 'participation', 'improvement_freq',
    'challenge', 'guidance_source', 'readiness', 'suggestions',
    'CRI', 'CRI_tier', 'engagement_score', 'has_trained',
    'n_important_skills', 'skills_gap'
]

df_sql = df[sql_cols].copy()
df_sql = df_sql.rename(columns={
    'sr_no': 'response_id',
    'CRI': 'cri',
    'CRI_tier': 'cri_tier'
})

# Convert boolean to int for SQLite
df_sql['has_trained'] = df_sql['has_trained'].astype(int)

# Connect & load
conn = sqlite3.connect(DB_PATH)
df_sql.to_sql('responses', conn, if_exists='replace', index=False)

# Verify
count = pd.read_sql("SELECT COUNT(*) as n FROM responses", conn)
print(f"\n✓ Loaded {count['n'][0]} rows into 'responses' table")
print(f"✓ Database: {DB_PATH}")

# Show schema
schema = pd.read_sql("PRAGMA table_info(responses)", conn)
print(f"\n✓ Table columns: {len(schema)}")
for _, row in schema.iterrows():
    print(f"    {row['name']:25s} {row['type']}")

conn.close()
print("\n" + "=" * 70)
print("DATABASE READY")
print("=" * 70)