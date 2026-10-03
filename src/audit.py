"""
Data Quality Audit Script
Purpose: Inspect responses.csv to understand structure, missing values, and issues.
Author: Disha Nate
Date: 2026-10-03
"""

import pandas as pd
from pathlib import Path

# --- 1. Set up paths (using Path for cross-platform compatibility) ---
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA = PROJECT_ROOT / "data" / "raw" / "responses.csv"

print("=" * 70)
print("CAREER READINESS SURVEY — DATA QUALITY AUDIT")
print("=" * 70)
print(f"\nLoading file: {RAW_DATA}\n")

# --- 2. Load the CSV ---
df = pd.read_csv(RAW_DATA)

# --- 3. Basic structure ---
print("=" * 70)
print("BASIC STRUCTURE")
print("=" * 70)
print(f"Rows:    {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"\nColumn names:")
for i, col in enumerate(df.columns, start=1):
    print(f"  {i:2d}. {col.strip()}")

# --- 4. Data types and missing values ---
print("\n" + "=" * 70)
print("MISSING VALUES & DATA TYPES")
print("=" * 70)

summary = pd.DataFrame({
    "dtype": df.dtypes.astype(str),
    "non_null": df.notna().sum(),
    "null_count": df.isna().sum(),
    "null_pct": (df.isna().mean() * 100).round(2),
})
print(summary.to_string())

# --- 5. Preview first 3 rows ---
print("\n" + "=" * 70)
print("FIRST 3 ROWS (key columns only)")
print("=" * 70)
preview_cols = df.columns[:6].tolist()  # first 6 columns only
print(df[preview_cols].head(3).to_string())

print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)