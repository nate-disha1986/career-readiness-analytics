-- ============================================================
-- Career Readiness Analytics — Database Schema
-- Author: Disha Nate
-- Purpose: Define structure for survey responses
-- ============================================================

DROP TABLE IF EXISTS responses;

CREATE TABLE responses (
    response_id              INTEGER PRIMARY KEY,
    timestamp                TEXT,
    age_group                TEXT,
    age_clean                TEXT,
    gender                   TEXT,
    education                TEXT,
    career_goal_clarity      TEXT,
    career_field             TEXT,
    career_path              TEXT,
    confidence               INTEGER,
    understanding            TEXT,
    important_skills         TEXT,
    skill_rating             INTEGER,
    participation            TEXT,
    improvement_freq         TEXT,
    challenge                TEXT,
    guidance_source          TEXT,
    readiness                INTEGER,
    suggestions              TEXT,
    cri                      REAL,
    cri_tier                 TEXT,
    engagement_score         REAL,
    has_trained              INTEGER,
    n_important_skills       INTEGER,
    skills_gap               INTEGER
);

-- Indexes for common query patterns
CREATE INDEX idx_age ON responses(age_clean);
CREATE INDEX idx_tier ON responses(cri_tier);
CREATE INDEX idx_gender ON responses(gender);
CREATE INDEX idx_trained ON responses(has_trained);