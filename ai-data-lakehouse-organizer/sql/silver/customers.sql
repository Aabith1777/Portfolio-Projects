CREATE OR REPLACE TABLE `silver.customers` AS

SELECT DISTINCT
    `CUST_ID` AS customer_id,
    `<PERSON_NAME>` AS <PERSON_NAME>,
    `<EMAIL_ADDRESS>` AS <EMAIL_ADDRESS>,
    COALESCE(
        SAFE.PARSE_DATE('%Y-%m-%d', `JOIN_DT`),
        SAFE.PARSE_DATE('%d-%m-%Y', `JOIN_DT`),
        SAFE.PARSE_DATE('%d/%m/%Y', `JOIN_DT`),
        SAFE.PARSE_DATE('%Y/%m/%d', `JOIN_DT`),
        SAFE.PARSE_DATE('%m-%d-%Y', `JOIN_DT`),
        SAFE.PARSE_DATE('%b %d %Y', `JOIN_DT`)
    ) AS registration_date

FROM `bronze.cust_info_final`;
