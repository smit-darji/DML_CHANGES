--liquibase formatted sql

--changeset 12:0010-create-agile-reporting-1testing222222222222222222222222

use database DEV_RZ;
use schema ACCOUNTING_ANALYTICS;
use role FULL_ACCESS_ROLE;
use warehouse SNOWFLAKE_LEARNING_WH;

CREATE TABLE IF NOT EXISTS DEV_RZ.ACCOUNTING_ANALYTICS.demoo222222222222o(
    ID             NUMBER       PRIMARY KEY,
    NAME           STRING       NOT NULL,
    STATUS         STRING,
    CREATED_AT     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

