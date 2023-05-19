{{ config(materialized='table') }}

WITH green_taxi_rides AS 
(
  SELECT 
        *,
        'Green' as service_type 
  FROM {{ ref('stg_green_tripdata') }}
),

yellow_taxi_rides AS 
(
  SELECT 
        *,
        'Yellow' as service_type 
  FROM {{ ref('stg_yellow_tripdata') }}
),

all_trips AS (
    SELECT * FROM green_taxi_rides
    UNION ALL
    SELECT * FROM yellow_taxi_rides
),

dim_zones AS (
    SELECT * FROM{{ ref('dim_zones') }}
)

SELECT
    trip_id,
    VendorID,
    service_type,
    RatecodeID,
    ratecodeid_desc,
    PULocationID,
    pickup_location.Borough as pickup_location_borough,
    pickup_location.Zone as pickup_location_zone,
    DOLocationID,
    dropoff_location.Borough as dropoff_location_borough,
    dropoff_location.Zone as dropoff_location_zone,
    pickup_datetime,
    dropoff_datetime,
    store_and_fwd_flag,
    passenger_count,
    trip_distance,
    trip_type,
    trip_type_desc,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    ehail_fee,
    improvement_surcharge,
    total_amount,
    payment_type,
    payment_type_desc,
    congestion_surcharge,
    airport_fee
FROM 
    all_trips
INNER JOIN
    dim_zones AS pickup_location ON all_trips.PULocationID = pickup_location.LocationID
INNER JOIN
    dim_zones AS dropoff_location ON all_trips.DOLocationID = dropoff_location.LocationID