"""
Career Readiness Analytics — Interactive Dashboard
Author: Disha Nate
Deploy: Streamlit Community Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Career Readiness Index",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand palette
PRIMARY = "#1F4E79"
ACCENT  = "#E8720C"
SUCCESS = "#2E8B57"
DANGER  = "#C0392B"
GRAY    = "#7F8C8D"

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / "data" / "processed" / "responses_enriched.csv"
    return pd.read_csv(path)

df = load_data()

# ============================================================
# HEADER
# ============================================================
st.title("📊 Career Readiness Index (CRI) — Interactive Dashboard")
st.caption(
    f"Exploring **{len(df)} survey responses** | "
    "Built with Python + Streamlit | Author: Disha Nate"
)

# ============================================================
# KPI ROW
# ============================================================
k1, k2, k3, k4, k5 = st.columns(5)

avg_cri = df["CRI"].mean()
pct_ready = (df["CRI_tier"] == "Highly Ready").mean() * 100
pct_at_risk = (df["CRI_tier"] == "At Risk").mean() * 100
pct_trained = df["has_trained"].mean() * 100

k1.metric("Total Respondents", f"{len(df)}")
k2.metric("Avg CRI", f"{avg_cri:.1f}")
k3.metric("Highly Ready", f"{pct_ready:.1f}%")
k4.metric("At Risk", f"{pct_at_risk:.1f}%")
k5.metric("Trained", f"{pct_trained:.1f}%")

st.divider()

# ============================================================
# SIDEBAR — FILTERS
# ============================================================
with st.sidebar:
    st.header("🔍 Filters")

    age_options = sorted(df["age_clean"].dropna().unique().tolist())
    age_filter = st.multiselect("Age Group", age_options, default=age_options)

    gender_options = sorted(df["gender"].dropna().unique().tolist())
    gender_filter = st.multiselect("Gender", gender_options, default=gender_options)

    tier_options = ["At Risk", "Developing", "Proficient", "Highly Ready"]
    tier_filter = st.multiselect("CRI Tier", tier_options, default=tier_options)

    st.divider()
    st.caption("Built by Disha Nate · 2026")

# Apply filters
filtered = df[
    df["age_clean"].isin(age_filter)
    & df["gender"].isin(gender_filter)
    & df["CRI_tier"].isin(tier_filter)
].copy()

st.info(f"📌 Showing **{len(filtered)}** of **{len(df)}** respondents")

# ============================================================
# ROW 1 — CRI DISTRIBUTION + TIER PIE
# ============================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("CRI Distribution")
    fig = px.histogram(
        filtered, x="CRI", nbins=20,
        color_discrete_sequence=[PRIMARY]
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Career Readiness Index",
        yaxis_title="Respondents",
        height=350,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Tier Breakdown")
    tier_counts = filtered["CRI_tier"].value_counts()
    fig = px.pie(
        values=tier_counts.values,
        names=tier_counts.index,
        color=tier_counts.index,
        color_discrete_map={
            "At Risk": DANGER,
            "Developing": ACCENT,
            "Proficient": PRIMARY,
            "Highly Ready": SUCCESS
        },
        hole=0.4
    )
    fig.update_layout(height=350, margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ROW 2 — TRAINING IMPACT + ENGAGEMENT
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 Training Impact")
    train = filtered.groupby("has_trained")["CRI"].mean().reset_index()
    train["Status"] = train["has_trained"].map({0: "Not Trained", 1: "Trained"})
    fig = px.bar(
        train, x="Status", y="CRI",
        color="Status",
        color_discrete_map={"Not Trained": DANGER, "Trained": SUCCESS},
        text_auto=".1f"
    )
    fig.update_layout(showlegend=False, height=350, margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Engagement vs Readiness")
    # Create engagement band on the fly
    filtered = filtered.copy()
    filtered["engagement_band"] = pd.cut(
        filtered["engagement_score"],
        bins=[-1, 50, 80, 101],
        labels=["Low", "Medium", "High"]
    )
    eng = filtered.groupby("engagement_band", observed=True)["CRI"].mean().reindex(
        ["Low", "Medium", "High"]
    ).dropna().reset_index()
    fig = px.bar(
        eng, x="engagement_band", y="CRI",
        color="engagement_band",
        color_discrete_map={"Low": DANGER, "Medium": ACCENT, "High": SUCCESS},
        text_auto=".1f"
    )
    fig.update_layout(showlegend=False, height=350, margin=dict(t=20, b=20),
                      xaxis_title="Engagement Level", yaxis_title="Avg CRI")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ROW 3 — CRI BY AGE + BY FIELD
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Readiness by Age Group")
    age_avg = filtered.groupby("age_clean")["CRI"].mean().reset_index()
    fig = px.bar(age_avg, x="age_clean", y="CRI",
                 color_discrete_sequence=[PRIMARY], text_auto=".1f")
    fig.update_layout(showlegend=False, height=350, margin=dict(t=20, b=20),
                      xaxis_title="", yaxis_title="Avg CRI")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎓 Readiness by Career Field")
    field = (filtered.groupby("career_field")
             .agg(n=("CRI", "size"), avg_cri=("CRI", "mean"))
             .query("n >= 3")
             .sort_values("avg_cri", ascending=True)
             .reset_index())
    fig = px.bar(field, x="avg_cri", y="career_field", orientation="h",
                 color="avg_cri", color_continuous_scale=["#C0392B", "#E8720C", "#2E8B57"],
                 text_auto=".1f")
    fig.update_layout(height=350, margin=dict(t=20, b=20), showlegend=False,
                      coloraxis_showscale=False,
                      xaxis_title="Avg CRI", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ROW 4 — TOP CHALLENGES
# ============================================================
st.subheader("⚠️ Top Challenges Faced")

challenges = (filtered["challenge"].dropna()
              .astype(str).str.split(",").explode().str.strip())
challenges = challenges[challenges != ""].value_counts().head(10).reset_index()
challenges.columns = ["Challenge", "Count"]

fig = px.bar(challenges, x="Count", y="Challenge", orientation="h",
             color_discrete_sequence=[DANGER], text_auto=True)
fig.update_layout(height=400, margin=dict(t=20, b=20), yaxis_title="",
                  yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption(
    "**Methodology:** CRI = 50%×readiness + 25%×confidence + 25%×skill_rating "
    "(scaled 0–100). Tiers: At Risk (0–40), Developing (40–60), "
    "Proficient (60–80), Highly Ready (80–100)."
)