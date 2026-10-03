# Data Dictionary — Career Readiness Survey

**Source:** Google Forms survey
**Collection period:** Aug–Sep 2026
**Total responses:** 121
**Total questions:** 19

---

## Column Reference

| # | Column | Type | Values / Range | Missing | Notes |
|---|--------|------|----------------|---------|-------|
| 1 | Sr.No. | Integer | 1–121 | 0% | Respondent ID |
| 2 | Timestamp | DateTime | 12/08/2026 onwards | 0% | Submission time |
| 3 | Name | String | Free text | 0% | **PII — dropped before analysis** |
| 4 | Age Group | Categorical | Mixed (18–20, 21–23, 24–26, Above 26, Below 18, numeric like 53, 40) | 0% | **Needs standardization** |
| 5 | Gender | Categorical | Male / Female | 0% | Clean |
| 6 | Education Level | Categorical | Undergraduate, Postgraduate, Higher Secondary, Professional/Technical, Graduate, Diploma, School | 0% | Minor casing inconsistencies |
| 7 | Career Goal Clarity | Categorical | "Yes, clearly defined" / "General idea" / "Still exploring" / "Not decided" | 0% | Clean |
| 8 | Career Field | Categorical | IT/CS, Business, Engineering, Healthcare, Media, Government, Finance, etc. | 0% | Free text in some rows — needs normalization |
| 9 | Career Path | Categorical | Private-sector, Government, Higher Education, Entrepreneurship, Freelancing, Internship, Still undecided | 0% | Clean |
| 10 | Confidence | Ordinal (1–5) | 1, 2, 3, 4, 5 | 0% | Numeric — core CRI component |
| 11 | Understanding | Categorical | "Very well" / "Well" / "Moderately" / "Slightly" / "Not at all" | 0% | Clean |
| 12 | Important Skills | Multi-select (CSV) | 9 possible skill tokens | 0% | **Explode for analysis** |
| 13 | Skill Rating | Ordinal (1–5) | 1, 2, 3, 4, 5 | 0% | Numeric — core CRI component |
| 14 | Participation | Categorical | "Yes, multiple times" / "Yes, once" / "Currently participating" / "No, but I plan to" / "No, I have not participated" | 0% | Clean |
| 15 | Improvement Freq | Categorical | Daily / Several times a week / Weekly / Occasionally / Rarely / Never | 0% | Clean |
| 16 | Challenge | Multi-select (CSV) | 10 possible challenge tokens | 0% | **Explode for analysis** |
| 17 | Guidance Source | Multi-select (CSV) | 9 possible source tokens | 0% | **Explode for analysis** |
| 18 | Readiness | Ordinal (1–5) | 1, 2, 3, 4, 5 | 0% | Numeric — core CRI component |
| 19 | Suggestions | Free text | Open-ended | 47% | Optional field — will NLP-analyze |

---

## Derived Features (to be created)

| Feature | Formula | Purpose |
|---------|---------|---------|
| `age_clean` | Standardized buckets | Group comparisons |
| `CRI` | Weighted composite: 0.5×readiness + 0.25×confidence + 0.25×skill_rating (scaled 0–100) | Single readiness metric |
| `CRI_tier` | Bins: At Risk (0–40), Developing (40–60), Proficient (60–80), Highly Ready (80–100) | Segment response |
| `engagement_score` | 0.6×improvement_freq + 0.4×participation | Behavioral metric |
| `segment` | K-means clustering (k=4) | Persona identification |

---

## Privacy & Ethics

- **PII handling:** The `Name` column is dropped before any analysis and never committed to GitHub.
- **Data storage:** Raw data (`responses.csv`) is git-ignored and stays local only.
- **Consent:** Responses were collected via a survey with implied consent for analysis.
- **Bias acknowledgment:** Convenience sample of 121, primarily 18–23, majority female. Findings are exploratory, not population-inferential.

---

*Last updated: 2026-10-03 | Author: Disha Nate*