"""
Executive Visualization Script
Purpose: Create publication-grade charts for executive reporting.
Author: Disha Nate
Date: 2026-10-03
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Brand palette ---
BRAND = {
    "primary": "#1F4E79",      # Deep blue
    "accent":  "#E8720C",      # Orange
    "success": "#2E8B57",      # Green
    "danger":  "#C0392B",      # Red
    "gray":    "#7F8C8D",
    "bg":      "#FAFAFA"
}

# --- Setup ---
PROJECT_ROOT = Path(__file__).parent.parent
DATA = PROJECT_ROOT / "data" / "processed" / "responses_enriched.csv"
FIG_DIR = PROJECT_ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Style
sns.set_style("whitegrid")
plt.rcParams.update({
    "figure.facecolor": BRAND["bg"],
    "axes.facecolor": BRAND["bg"],
    "axes.edgecolor": BRAND["gray"],
    "axes.labelcolor": BRAND["primary"],
    "axes.titleweight": "bold",
    "axes.titlesize": 14,
    "font.size": 10,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.facecolor": BRAND["bg"],
})

df = pd.read_csv(DATA)
print(f"Loaded {len(df)} rows")

# ============================================================
# CHART 1 — CRI Distribution (histogram)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.hist(df["CRI"], bins=20, color=BRAND["primary"], edgecolor="white", alpha=0.85)
ax.axvline(df["CRI"].mean(), color=BRAND["accent"], linestyle="--", linewidth=2,
           label=f"Mean CRI = {df['CRI'].mean():.1f}")
ax.set_title("Career Readiness Index Distribution Across 121 Respondents", pad=15)
ax.set_xlabel("Career Readiness Index (0–100)")
ax.set_ylabel("Number of Respondents")
ax.legend()
plt.savefig(FIG_DIR / "01_cri_distribution.png")
plt.close()
print("✓ Chart 1: CRI Distribution")

# ============================================================
# CHART 2 — Average CRI by Age Group
# ============================================================
age_order = ["Under 18", "18-20", "21-23", "24-26", "Above 26"]
age_cri = df.groupby("age_clean")["CRI"].mean().reindex(age_order).dropna()

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(age_cri.index, age_cri.values, color=BRAND["primary"], edgecolor="white")
# Color the lowest bar red, highest green
min_idx = age_cri.values.argmin()
max_idx = age_cri.values.argmax()
bars[min_idx].set_color(BRAND["danger"])
bars[max_idx].set_color(BRAND["success"])
for bar, val in zip(bars, age_cri.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.1f}",
            ha="center", fontweight="bold", color=BRAND["primary"])
ax.set_title("Average CRI by Age Group: Readiness Peaks at 24–26", pad=15)
ax.set_xlabel("Age Group")
ax.set_ylabel("Average CRI")
ax.set_ylim(0, 100)
plt.savefig(FIG_DIR / "02_cri_by_age.png")
plt.close()
print("✓ Chart 2: CRI by Age")

# ============================================================
# CHART 3 — Training Impact
# ============================================================
train = df.groupby("has_trained")["CRI"].mean()
labels = ["Not Trained", "Trained"]
values = [train[False], train[True]]

fig, ax = plt.subplots(figsize=(8, 5.5))
bars = ax.bar(labels, values, color=[BRAND["danger"], BRAND["success"]], edgecolor="white", width=0.5)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.1f}",
            ha="center", fontweight="bold", color=BRAND["primary"], fontsize=12)
ax.set_title("Training Impact on Readiness:\n+8.6 CRI Points for Trained Respondents", pad=15)
ax.set_ylabel("Average CRI")
ax.set_ylim(0, 100)
plt.savefig(FIG_DIR / "03_training_impact.png")
plt.close()
print("✓ Chart 3: Training Impact")

# ============================================================
# CHART 4 — Engagement vs CRI
# ============================================================
def engagement_band(score):
    if score >= 80: return "High"
    if score >= 50: return "Medium"
    return "Low"

df["engagement_band"] = df["engagement_score"].apply(engagement_band)
eng = df.groupby("engagement_band")["CRI"].mean().reindex(["Low", "Medium", "High"])

fig, ax = plt.subplots(figsize=(8, 5.5))
bars = ax.bar(eng.index, eng.values,
              color=[BRAND["danger"], BRAND["accent"], BRAND["success"]],
              edgecolor="white", width=0.5)
for bar, val in zip(bars, eng.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.1f}",
            ha="center", fontweight="bold", color=BRAND["primary"], fontsize=12)
ax.set_title("Engagement Drives Readiness:\n23-Point CRI Gap Between High & Low Engagement", pad=15)
ax.set_ylabel("Average CRI")
ax.set_ylim(0, 100)
plt.savefig(FIG_DIR / "04_engagement_vs_cri.png")
plt.close()
print("✓ Chart 4: Engagement vs CRI")

# ============================================================
# CHART 5 — Top Challenges (multi-select explode)
# ============================================================
challenges = (df["challenge"].dropna()
              .astype(str)
              .str.split(",")
              .explode()
              .str.strip())
challenges = challenges[challenges != ""]
top_challenges = challenges.value_counts().head(10)

fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(top_challenges.index[::-1], top_challenges.values[::-1],
        color=BRAND["primary"], edgecolor="white")
for i, val in enumerate(top_challenges.values[::-1]):
    ax.text(val + 0.3, i, str(val), va="center", fontweight="bold", color=BRAND["primary"])
ax.set_title("Top 10 Challenges Facing Respondents", pad=15)
ax.set_xlabel("Number of Mentions")
plt.savefig(FIG_DIR / "05_top_challenges.png")
plt.close()
print("✓ Chart 5: Top Challenges")

# ============================================================
# CHART 6 — Guidance Sources
# ============================================================
guides = (df["guidance_source"].dropna()
          .astype(str).str.split(",").explode().str.strip())
guides = guides[guides != ""]
top_guides = guides.value_counts().head(10)

fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(top_guides.index[::-1], top_guides.values[::-1],
        color=BRAND["accent"], edgecolor="white")
for i, val in enumerate(top_guides.values[::-1]):
    ax.text(val + 0.3, i, str(val), va="center", fontweight="bold", color=BRAND["primary"])
ax.set_title("Preferred Sources of Career Guidance", pad=15)
ax.set_xlabel("Number of Mentions")
plt.savefig(FIG_DIR / "06_guidance_sources.png")
plt.close()
print("✓ Chart 6: Guidance Sources")

# ============================================================
# CHART 7 — Career Field Readiness
# ============================================================
field_stats = (df.groupby("career_field")
               .agg(n=("CRI", "size"), avg_cri=("CRI", "mean"))
               .query("n >= 3")
               .sort_values("avg_cri", ascending=True))

fig, ax = plt.subplots(figsize=(11, 6))
colors = [BRAND["success"] if x >= 70 else BRAND["accent"] if x >= 60 else BRAND["danger"]
          for x in field_stats["avg_cri"]]
ax.barh(field_stats.index, field_stats["avg_cri"], color=colors, edgecolor="white")
for i, (val, n) in enumerate(zip(field_stats["avg_cri"], field_stats["n"])):
    ax.text(val + 0.8, i, f"{val:.1f} (n={n})", va="center", fontweight="bold",
            color=BRAND["primary"], fontsize=9)
ax.set_title("Average CRI by Career Field:\nIT/CS is Largest But Lowest Readiness", pad=15)
ax.set_xlabel("Average CRI")
ax.set_xlim(0, 100)
plt.savefig(FIG_DIR / "07_field_readiness.png")
plt.close()
print("✓ Chart 7: Career Field Readiness")

# ============================================================
# CHART 8 — CRI Tier Pie
# ============================================================
tier_counts = df["CRI_tier"].value_counts().reindex(
    ["At Risk", "Developing", "Proficient", "Highly Ready"]
)
colors_pie = [BRAND["danger"], BRAND["accent"], BRAND["primary"], BRAND["success"]]

fig, ax = plt.subplots(figsize=(9, 6))
wedges, texts, autotexts = ax.pie(
    tier_counts.values,
    labels=tier_counts.index,
    autopct=lambda p: f"{p:.1f}%\n({int(round(p*sum(tier_counts.values)/100))})",
    colors=colors_pie,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 11, "fontweight": "bold"}
)
ax.set_title("Respondent Distribution Across CRI Tiers", pad=15)
plt.savefig(FIG_DIR / "08_cri_tiers.png")
plt.close()
print("✓ Chart 8: CRI Tiers")

print(f"\n✓ All charts saved to: {FIG_DIR}")