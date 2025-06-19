--liquibase formatted sql

--changeset SMIT:0010-create-agile-reporting-table012231312
use database DEV_RZ;
use schema ACCOUNTING_ANALYTICS;
use role FULL_ACCESS_ROLE;
use warehouse SNOWFLAKE_LEARNING_WH;

CREATE TABLE IF NOT EXISTS DEV_RZ.ACCOUNTING_ANALYTICS.smit (
    ID             NUMBER       PRIMARY KEY,
    NAME           STRING       NOT NULL,
    STATUS         STRING,
    CREATED_AT     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

