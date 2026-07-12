CREATE OR REPLACE TABLE `silver.products` AS

SELECT
    `PROD_CODE` AS product_id,
    TRIM(`PROD_NM`) AS product_name,
    LOWER(`CATEGORY`) AS category,
    `PRICE` AS unit_price,
    CASE
        WHEN `PRICE` <= 0 THEN TRUE
        ELSE FALSE
    END AS unit_price_quality_flag

FROM `bronze.product_master_old`;
