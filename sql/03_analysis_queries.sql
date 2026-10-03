-- ============================================================
-- Career Readiness Analytics — Business Analysis Queries
-- Author: Disha Nate
-- Purpose: Answer key stakeholder questions with SQL
-- ============================================================

-- ============================================================
-- QUERY 1: Overall Readiness Snapshot
-- "How ready is our population overall?"
-- ============================================================
SELECT
    COUNT(*)                                    AS total_respondents,
    ROUND(AVG(cri), 1)                          AS avg_cri,
    ROUND(MIN(cri), 1)                          AS min_cri,
    ROUND(MAX(cri), 1)                          AS max_cri,
    SUM(CASE WHEN cri_tier = 'Highly Ready' THEN 1 ELSE 0 END) AS highly_ready,
    SUM(CASE WHEN cri_tier = 'At Risk' THEN 1 ELSE 0 END)      AS at_risk
FROM responses;

-- ============================================================
-- QUERY 2: Readiness by Age Group
-- "Which age group is most/least ready?"
-- ============================================================
SELECT
    age_clean,
    COUNT(*)                                    AS n,
    ROUND(AVG(cri), 1)                          AS avg_cri,
    ROUND(AVG(readiness), 2)                    AS avg_readiness,
    ROUND(AVG(confidence), 2)                   AS avg_confidence,
    ROUND(AVG(skill_rating), 2)                 AS avg_skill
FROM responses
GROUP BY age_clean
ORDER BY avg_cri DESC;

-- ============================================================
-- QUERY 3: Training Impact — the headline business question
-- "Does training actually improve readiness?"
-- ============================================================
SELECT
    CASE WHEN has_trained = 1 THEN 'Trained' ELSE 'Not Trained' END AS training_status,
    COUNT(*)                AS n,
    ROUND(AVG(cri), 1)      AS avg_cri,
    ROUND(AVG(confidence), 2) AS avg_confidence,
    ROUND(AVG(readiness), 2) AS avg_readiness
FROM responses
GROUP BY has_trained
ORDER BY has_trained DESC;

-- ============================================================
-- QUERY 4: CRI Tier Distribution
-- "How is our population distributed across readiness tiers?"
-- ============================================================
SELECT
    cri_tier,
    COUNT(*)                                    AS n,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM responses), 1) AS pct
FROM responses
WHERE cri_tier IS NOT NULL
GROUP BY cri_tier
ORDER BY
    CASE cri_tier
        WHEN 'At Risk'       THEN 1
        WHEN 'Developing'    THEN 2
        WHEN 'Proficient'    THEN 3
        WHEN 'Highly Ready'  THEN 4
    END;

-- ============================================================
-- QUERY 5: Top Career Fields by Readiness
-- "Where is readiness concentrated?"
-- ============================================================
SELECT
    career_field,
    COUNT(*)                AS n,
    ROUND(AVG(cri), 1)      AS avg_cri
FROM responses
WHERE career_field IS NOT NULL AND career_field != ''
GROUP BY career_field
HAVING COUNT(*) >= 3
ORDER BY avg_cri DESC
LIMIT 10;

-- ============================================================
-- QUERY 6: Readiness by Gender
-- ============================================================
SELECT
    gender,
    COUNT(*)                AS n,
    ROUND(AVG(cri), 1)      AS avg_cri,
    ROUND(AVG(confidence), 2) AS avg_confidence
FROM responses
GROUP BY gender
HAVING COUNT(*) >= 3
ORDER BY avg_cri DESC;

-- ============================================================
-- QUERY 7: Engagement vs Readiness
-- "Do more engaged respondents have higher CRI?"
-- ============================================================
SELECT
    CASE
        WHEN engagement_score >= 80 THEN 'High Engagement'
        WHEN engagement_score >= 50 THEN 'Medium Engagement'
        ELSE 'Low Engagement'
    END                     AS engagement_band,
    COUNT(*)                AS n,
    ROUND(AVG(cri), 1)      AS avg_cri
FROM responses
GROUP BY engagement_band
ORDER BY avg_cri DESC;

-- ============================================================
-- QUERY 8: High Performers — who are they?
-- ============================================================
SELECT
    response_id,
    age_clean,
    gender,
    cri,
    cri_tier,
    engagement_score,
    participation
FROM responses
WHERE cri_tier = 'Highly Ready'
ORDER BY cri DESC
LIMIT 10;

-- ============================================================
-- QUERY 9: At-Risk Respondents — intervention targets
-- ============================================================
SELECT
    response_id,
    age_clean,
    gender,
    cri,
    confidence,
    skill_rating,
    readiness,
    has_trained
FROM responses
WHERE cri_tier = 'At Risk'
ORDER BY cri ASC;

-- ============================================================
-- QUERY 10: Window function — rank within age group
-- ============================================================
SELECT
    age_clean,
    response_id,
    cri,
    RANK() OVER (PARTITION BY age_clean ORDER BY cri DESC) AS rank_in_group
FROM responses
WHERE cri IS NOT NULL
ORDER BY age_clean, rank_in_group
LIMIT 20;   