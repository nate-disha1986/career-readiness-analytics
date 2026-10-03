"""
Feature Engineering Script
Purpose: Create derived features — CRI, CRI tier, engagement score, skills gap.
Author: Disha Nate
Date: 2026-10-03
"""

import pandas as pd
import numpy as np
from pathlib import Path

# --- 1. Paths ---
PROJECT_ROOT = Path(__file__).parent.parent
CLEAN_DATA = PROJECT_ROOT / "data" / "interim" / "cleaned.csv"
ENRICHED_DATA = PROJECT_ROOT / "data" / "processed" / "responses_enriched.csv"

print("=" * 70)
print("FEATURE ENGINEERING PIPELINE")
print("=" * 70)

# --- 2. Load cleaned data ---
print(f"\nLoading: {CLEAN_DATA}")
df = pd.read_csv(CLEAN_DATA)
print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ============================================================
# FEATURE 1: CAREER READINESS INDEX (CRI)
# ============================================================
print("\n[1] Building Career Readiness Index (CRI)...")
print("    Formula: CRI = 50%×readiness + 25%×confidence + 25%×skill_rating")

# Normalize each 1-5 rating to 0-1 scale
for col in ['readiness', 'confidence', 'skill_rating']:
    df[f'{col}_norm'] = (df[col] - 1) / 4

# Weighted composite (0-100 scale)
df['CRI'] = (
    0.50 * df['readiness_norm'] +
    0.25 * df['confidence_norm'] +
    0.25 * df['skill_rating_norm']
) * 100

df['CRI'] = df['CRI'].round(1)

# CRI Tier (categorical bucket)
df['CRI_tier'] = pd.cut(
    df['CRI'],
    bins=[0, 40, 60, 80, 100],
    labels=['At Risk', 'Developing', 'Proficient', 'Highly Ready'],
    include_lowest=True
)

print(f"    ✓ CRI created (range: {df['CRI'].min()}–{df['CRI'].max()})")
print(f"    ✓ Mean CRI: {df['CRI'].mean():.1f}")
print(f"    Tier distribution:")
for tier, count in df['CRI_tier'].value_counts().sort_index().items():
    pct = count / len(df) * 100
    print(f"      - {tier}: {count} ({pct:.1f}%)")

# ============================================================
# FEATURE 2: ENGAGEMENT SCORE
# ============================================================
print("\n[2] Building Engagement Score...")

# Map categorical to numeric
freq_map = {
    'Daily': 5,
    'Several times a week': 4,
    'Weekly': 3,
    'Occasionally': 2,
    'Rarely': 1,
    'Never': 0
}

participation_map = {
    'Yes, multiple times': 3,
    'Currently participating': 3,
    'Yes, once': 2,
    'No, but I plan to': 1,
    'No, I have not participated': 0
}

df['improvement_freq_score'] = df['improvement_freq'].map(freq_map).fillna(0)
df['participation_score'] = df['participation'].map(participation_map).fillna(0)

# Composite: 60% frequency + 40% participation, scaled 0-100
df['engagement_score'] = (
    0.60 * (df['improvement_freq_score'] / 5) +
    0.40 * (df['participation_score'] / 3)
) * 100

df['engagement_score'] = df['engagement_score'].round(1)

print(f"    ✓ Engagement Score created (range: {df['engagement_score'].min()}–{df['engagement_score'].max()})")
print(f"    ✓ Mean: {df['engagement_score'].mean():.1f}")

# ============================================================
# FEATURE 3: SKILLS GAP SCORE
# ============================================================
print("\n[3] Building Skills Gap Score...")

# How many skills does each respondent consider important?
df['n_important_skills'] = df['important_skills'].fillna('').apply(
    lambda x: len([s for s in str(x).split(',') if s.strip()]) if x else 0
)

# Gap = (skills desired) - (skill rating × 2)
# Higher gap = more ambition than current capability
df['skills_gap'] = df['n_important_skills'] - (df['skill_rating'] * 2)
df['skills_gap'] = df['skills_gap'].clip(lower=0)  # No negative gaps

print(f"    ✓ Skills Gap created (range: {df['skills_gap'].min()}–{df['skills_gap'].max()})")
print(f"    ✓ Mean: {df['skills_gap'].mean():.1f}")
print(f"    ✓ Average skills listed as important: {df['n_important_skills'].mean():.1f}")

# ============================================================
# FEATURE 4: TRAINING IMPACT FLAG
# ============================================================
print("\n[4] Building Training Impact flag...")

df['has_trained'] = df['participation'].str.contains(
    'Yes|Currently', case=False, na=False
)

print(f"    ✓ {df['has_trained'].sum()} respondents have training/internship experience")
print(f"    ✓ {len(df) - df['has_trained'].sum()} have not")

# ============================================================
# SAVE
# ============================================================
ENRICHED_DATA.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(ENRICHED_DATA, index=False)
print(f"\n✓ Enriched data saved: {ENRICHED_DATA}")
print(f"  Final shape: {df.shape[0]} rows × {df.shape[1]} columns")

print("\n" + "=" * 70)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 70)