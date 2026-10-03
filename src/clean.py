"""
Data Cleaning Script
Purpose: Transform raw survey responses into analysis-ready dataset.
Author: Disha Nate
Date: 2026-10-03
"""

import pandas as pd
import numpy as np
from pathlib import Path

# --- 1. Paths ---
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA = PROJECT_ROOT / "data" / "raw" / "responses.csv"
CLEAN_DATA = PROJECT_ROOT / "data" / "interim" / "cleaned.csv"

print("=" * 70)
print("DATA CLEANING PIPELINE")
print("=" * 70)

# --- 2. Load ---
print(f"\nLoading: {RAW_DATA}")
df = pd.read_csv(RAW_DATA)
print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# --- 3. Rename columns ---
print("\n[1] Renaming columns...")
df.columns = [
    'sr_no', 'timestamp', 'name', 'age_group', 'gender', 'education',
    'career_goal_clarity', 'career_field', 'career_path',
    'confidence', 'understanding', 'important_skills',
    'skill_rating', 'participation', 'improvement_freq',
    'challenge', 'guidance_source', 'readiness', 'suggestions'
]
print(f"    ✓ {len(df.columns)} columns renamed")

# --- 4. Drop PII (privacy) ---
print("\n[2] Dropping PII (Name column)...")
df = df.drop(columns=['name'])
print(f"    ✓ Name column removed (privacy safeguard)")

# --- 5. Standardize age groups ---
print("\n[3] Standardizing age groups...")
def clean_age(x):
    x = str(x).strip()
    if x == "Below 18":
        return "Under 18"
    if x in ["18–20", "18-20"]:
        return "18-20"
    if x in ["21–23", "21-23"]:
        return "21-23"
    if x in ["24–26", "24-26"]:
        return "24-26"
    if x == "Above 26":
        return "Above 26"
    try:
        age = int(x)
        if age < 18: return "Under 18"
        if age <= 20: return "18-20"
        if age <= 23: return "21-23"
        if age <= 26: return "24-26"
        return "Above 26"
    except (ValueError, TypeError):
        return "Unknown"

df['age_clean'] = df['age_group'].apply(clean_age)
print(f"    ✓ Created 'age_clean' column")
print(f"    Distribution: {df['age_clean'].value_counts().to_dict()}")

# --- 6. Trim whitespace on all text columns ---
print("\n[4] Trimming whitespace on text columns...")
text_cols = df.select_dtypes(include=['object', 'string']).columns
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
print(f"    ✓ {len(text_cols)} text columns cleaned")

# --- 7. Handle missing values ---
print("\n[5] Handling missing values...")
# Suggestions: fill NaN with empty string
df['suggestions'] = df['suggestions'].fillna('')
# Also treat "." ".." "..." "NA" as empty
df['suggestions'] = df['suggestions'].replace(['.', '..', '...', 'NA', 'N/A', 'na', 'no', '-'], '', regex=False)
print(f"    ✓ Suggestions: {len(df[df['suggestions'] == ''])} empty | {len(df[df['suggestions'] != ''])} have feedback")

# --- 8. Validate numeric columns ---
print("\n[6] Validating numeric columns (1-5 range)...")
for col in ['confidence', 'skill_rating', 'readiness']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    invalid = ((df[col] < 1) | (df[col] > 5)).sum()
    if invalid > 0:
        print(f"    ⚠ {col}: {invalid} values out of range — will handle")
    df[col] = df[col].fillna(df[col].median())
    print(f"    ✓ {col}: range [{df[col].min()}, {df[col].max()}], median = {df[col].median():.1f}")

# --- 9. Save ---
CLEAN_DATA.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(CLEAN_DATA, index=False)
print(f"\n✓ Cleaned data saved: {CLEAN_DATA}")
print(f"  Final shape: {df.shape[0]} rows × {df.shape[1]} columns")

print("\n" + "=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)