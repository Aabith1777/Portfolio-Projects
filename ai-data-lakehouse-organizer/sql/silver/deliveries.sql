CREATE OR REPLACE TABLE `silver.deliveries` AS

SELECT
    `TRACK_ID` AS tracking_id,
    `ORDER_REFERENCE` AS order_id,
    `COURIER_NM` AS courier_name,
    COALESCE(
        SAFE.PARSE_DATE('%Y-%m-%d', `SHIP_DT`),
        SAFE.PARSE_DATE('%d-%m-%Y', `SHIP_DT`),
        SAFE.PARSE_DATE('%d/%m/%Y', `SHIP_DT`),
        SAFE.PARSE_DATE('%Y/%m/%d', `SHIP_DT`),
        SAFE.PARSE_DATE('%m-%d-%Y', `SHIP_DT`),
        SAFE.PARSE_DATE('%b %d %Y', `SHIP_DT`)
    ) AS shipment_date,
    LOWER(`DELIVERY_STATUS`) AS delivery_status

FROM `bronze.delivery_tracking`;
