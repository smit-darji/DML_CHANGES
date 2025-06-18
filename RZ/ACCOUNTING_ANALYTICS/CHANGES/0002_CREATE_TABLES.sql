--liquibase formatted sql

--changeset yourname:0010-create-agile-reporting-table71

CREATE TABLE IF NOT EXISTS AGILE_REPORTING.TASKS (
    ID             NUMBER       PRIMARY KEY,
    NAME           STRING       NOT NULL,
    STATUS         STRING,
    CREATED_AT     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
