{{ config(materialized='table') }}

SELECT 
    LocationID,
    Borough,
    Zone,
    REPLACE(service_zone, 'Boro', 'Green') as service_zone
FROM
    {{ ref ('taxi_zone_lookup') }}