CREATE OR REPLACE TABLE `silver.order_items` AS

SELECT
    `ITEM_ID` AS order_item_id,
    `ORDER_REF` AS order_id,
    `PRODUCT_REF` AS product_id,
    `QTY` AS quantity,
    CASE
        WHEN `QTY` <= 0 THEN TRUE
        ELSE FALSE
    END AS quantity_quality_flag,
    `UNIT_PRICE` AS unit_price

FROM `bronze.order_items_new`;
