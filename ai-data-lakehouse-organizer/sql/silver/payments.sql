CREATE OR REPLACE TABLE `silver.payments` AS

SELECT DISTINCT
    `PAYMENT_ID` AS payment_id,
    `ORDER_ID_REF` AS order_id,
    LOWER(`PAY_MODE`) AS payment_method,
    `PAYMENT_AMT` AS payment_amount,
    LOWER(`PAYMENT_STATUS`) AS payment_status

FROM `bronze.payment_txns_v2`;
