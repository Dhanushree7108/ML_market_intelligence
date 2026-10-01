-- Milestone 1 schema
-- Run this inside the ml_project database (pgAdmin Query Tool or psql)

CREATE TABLE IF NOT EXISTS projects (
    id                    SERIAL PRIMARY KEY,
    project_name          VARCHAR(200)   NOT NULL,
    project_description   TEXT           NOT NULL,
    target_market         TEXT           NOT NULL,
    budget                NUMERIC(15,2)  NOT NULL,
    competition           TEXT,
    resources             TEXT,
    objectives            TEXT,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quick sanity check after submitting a project from the form:
-- SELECT * FROM projects ORDER BY id DESC;
