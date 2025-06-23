--liquibase formatted sql

--changeset DEMO:0010-create-agile-reporting-5555

use database DEV_RZ;
use schema AGILE_REPORTING;
use role FULL_ACCESS_ROLE;
use warehouse SNOWFLAKE_LEARNING_WH;


CREATE TABLE IF NOT EXISTS DEV_RZ.ACCOUNTING_ANALYTICS.demo5555 (
    ID             NUMBER       PRIMARY KEY,
    NAME           STRING       NOT NULL,
    STATUS         STRING,
    CREATED_AT     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
