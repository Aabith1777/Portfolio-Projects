CREATE OR REPLACE TABLE `silver.orders` AS

SELECT
    `ORD_ID` AS order_id,
    `CUST_REF` AS customer_id,
    COALESCE(
        SAFE.PARSE_DATE('%Y-%m-%d', `ORD_DT`),
        SAFE.PARSE_DATE('%d-%m-%Y', `ORD_DT`),
        SAFE.PARSE_DATE('%d/%m/%Y', `ORD_DT`),
        SAFE.PARSE_DATE('%Y/%m/%d', `ORD_DT`),
        SAFE.PARSE_DATE('%m-%d-%Y', `ORD_DT`),
        SAFE.PARSE_DATE('%b %d %Y', `ORD_DT`)
    ) AS order_date,
    LOWER(`ORDER_STATUS`) AS order_status,
    `TOTAL_AMT` AS total_amount

FROM `bronze.order_dump_2025`;
