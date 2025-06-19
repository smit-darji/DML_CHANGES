--liquibase formatted sql

--changeset yourname:0010-create-agile-reporting-table01

use database DEV_RZ;
use schema AGILE_REPORTING;
CREATE TABLE IF NOT EXISTS DEV_RZ.AGILE_REPORTING.TASKS (
    ID             NUMBER       PRIMARY KEY,
    NAME           STRING       NOT NULL,
    STATUS         STRING,
    CREATED_AT     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE DEV_RZ.AGILE_REPORTING.TASKS
ADD COLUMN DESCRIPTION STRING;