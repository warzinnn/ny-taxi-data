{{ config(materialized='view') }}

WITH tripdata AS 
(
  SELECT *,
    row_number() OVER(PARTITION BY VendorID, PULocationID, DOLocationID, pickup_datetime, dropoff_datetime, passenger_count) AS rn
  FROM {{ source('staging', 'green-taxi-data') }}
)

SELECT 
    VendorID,
    {{ dbt_utils.generate_surrogate_key(['VendorID', 'PULocationID', 'DOLocationID', 'pickup_datetime', 'dropoff_datetime', 'passenger_count']) }} AS trip_id,
    pickup_datetime,
    dropoff_datetime,
    store_and_fwd_flag,
    RatecodeID,
    {{ get_rate_code_description("RatecodeID") }} AS ratecodeid_desc,
    PULocationID,
    DOLocationID,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    ehail_fee,
    improvement_surcharge,
    total_amount,
    payment_type,
    {{ get_payment_type_description("payment_type") }} AS payment_type_desc,
    trip_type,
    {{ get_trip_type_description("trip_type") }} AS trip_type_desc,
    congestion_surcharge,
    CAST(0.0 AS FLOAT64) AS airport_fee
FROM 
    tripdata
WHERE
    rn = 1 -- unique trip_id
{% if var('is_test', default=true) %}
    LIMIT 100
{% endif %}