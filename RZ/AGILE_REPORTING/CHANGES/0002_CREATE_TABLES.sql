--liquibase formatted sql

--changeset yourname:0010-create-agile-reporting-table01

CREATE TABLE IF NOT EXISTS DEV_RZ.ACCOUNTING_ANALYTICS.TASKS (
    ID             NUMBER       PRIMARY KEY,
    NAME           STRING       NOT NULL,
    STATUS         STRING,
    CREATED_AT     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
