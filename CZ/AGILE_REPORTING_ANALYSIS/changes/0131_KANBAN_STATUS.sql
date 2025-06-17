--liquibase formatted sql

CREATE OR REPLACE VIEW VW_KANBAN_STATUS (
    PROJECT_KEY,
    PROJECT_NAME,
    WEEK,
    YEAR,
    FIRST_DAY_OF_WEEK,
    ISSUE_STATUS,
    ISSUE_COUNT,
    CREATED_DATE,
    UPDATED_DATE
    
) as

WITH KANBAN_STATUS AS (

    SELECT
    PROJECT_KEY
    , PROJECT_NAME
    , WEEK
    , YEAR
    , FIRST_DAY_OF_WEEK
    , TOTAL_CREATED_ISSUES                AS "Created"
    , TOTAL_OPEN_ISSUES                   AS "Open"
    , TOTAL_READY_FOR_REFINEMENT_ISSUES   AS "Ready for Refinement"
    , TOTAL_READY_FOR_WORK_ISSUES         AS "Ready For Work"
    , TOTAL_WORKING_ISSUES                AS "Working"
    , TOTAL_IN_QA_ISSUES                  AS "In QA"
    , TOTAL_PEER_REVIEW_ISSUES            AS "Peer Review"
    , TOTAL_IN_UAT_ISSUES                 AS "In UAT"
    , TOTAL_READY_FOR_DEPLOYEMENT_ISSUES  AS "Ready For Deployment"
    , CREATED_DATE
    , UPDATED_DATE
    FROM ${envId}_CZ.AGILE_REPORTING_MAIN.KANBAN_METRICS
)
    
SELECT 
    PROJECT_KEY,
    PROJECT_NAME,
    WEEK,
    YEAR,
    FIRST_DAY_OF_WEEK,
    ISSUE_STATUS,
    ISSUE_COUNT,
    CREATED_DATE,
    UPDATED_DATE
    
FROM KANBAN_STATUS
UNPIVOT (
    ISSUE_COUNT FOR ISSUE_STATUS IN (
        "Created",
        "Open",
        "Ready for Refinement",
        "Ready For Work",
        "Working",
        "In QA",
        "Peer Review",
        "In UAT",
        "Ready For Deployment"
    )
);

-- Grant Access to Views
grant select on VW_KANBAN_STATUS to role ANALYST;
