--liquibase formatted sql

--changeset yourname:0010-create-agile-reporting-table01
use database DEV_RZ;
use schema ACCOUNTING_ANALYTICS;
ALTER TABLE DEV_RZ.ACCOUNTING_ANALYTICS.TASKS
ADD COLUMN DESCRIPTION STRING;
