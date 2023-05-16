from prefect import flow, task
from numpy import int32, float64
import pandas as pd

@task(name="clean-data")
def clean_taxi_data(df):
    """Task to fix dtype issues"""
    if 'VendorID' in df.columns:
        print(f"pre: missing VendorID count: {df.VendorID.isna().sum()}")
        df.VendorID.fillna(0, inplace=True)
        print(f"post: missing VendorID count: {df.VendorID.isna().sum()}")
        df.VendorID = df.VendorID.astype(int32)
    
    if 'tpep_pickup_datetime' in df.columns and 'tpep_dropoff_datetime' in df.columns:
        # For yellow taxis
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.rename(columns = {'tpep_pickup_datetime':'pickup_datetime', 'tpep_dropoff_datetime':'dropoff_datetime'}, inplace = True)
    elif 'lpep_pickup_datetime' in df.columns and 'lpep_dropoff_datetime' in df.columns:
        # For green taxis
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.rename(columns = {'lpep_pickup_datetime':'pickup_datetime', 'lpep_dropoff_datetime':'dropoff_datetime'}, inplace = True)
    
    if 'passenger_count' in df.columns:
        print(f"pre: missing passenger_count count: {df.passenger_count.isna().sum()}")
        df.passenger_count.fillna(0, inplace=True)
        print(f"post: missing passenger_count count: {df.passenger_count.isna().sum()}")
        df.passenger_count = df.passenger_count.astype(int32)

    if 'trip_distance' in df.columns:
        print(f"pre: missing trip_distance count: {df.trip_distance.isna().sum()}")
        df.trip_distance.fillna(0.0, inplace=True)
        print(f"post: missing trip_distance count: {df.trip_distance.isna().sum()}")
        df.trip_distance = df.trip_distance.astype(float64)

    if 'RatecodeID' in df.columns:
        print(f"pre: missing RatecodeID count: {df.RatecodeID.isna().sum()}")
        df.RatecodeID.fillna(0, inplace=True)
        print(f"post: missing RatecodeID count: {df.RatecodeID.isna().sum()}")
        df.RatecodeID = df.RatecodeID.astype(int32)

    if 'store_and_fwd_flag' in df.columns:
        print(f"pre: missing store_and_fwd_flag count: {df.store_and_fwd_flag.isna().sum()}")
        df.store_and_fwd_flag.fillna(0, inplace=True)
        print(f"post: missing store_and_fwd_flag count: {df.store_and_fwd_flag.isna().sum()}")
        df.store_and_fwd_flag = df.store_and_fwd_flag.astype("string")

    if 'PULocationID' in df.columns and 'DOLocationID' in df.columns:
        print(f"pre: missing PULocationID count: {df.PULocationID.isna().sum()}")
        df.PULocationID.fillna(264, inplace=True)
        print(f"post: missing PULocationID count: {df.PULocationID.isna().sum()}")
        df.PULocationID = df.PULocationID.astype(int32)
        
        print(f"pre: missing DOLocationID count: {df.DOLocationID.isna().sum()}")
        df.DOLocationID.fillna(264, inplace=True)
        print(f"post: missing DOLocationID count: {df.DOLocationID.isna().sum()}")
        df.DOLocationID = df.DOLocationID.astype(int32)

    if 'payment_type' in df.columns:
        print(f"pre: missing payment_type count: {df.payment_type.isna().sum()}")
        df.payment_type.fillna(0, inplace=True)
        print(f"post: missing payment_type count: {df.payment_type.isna().sum()}")
        df.payment_type = df.payment_type.astype(int32)

    rest_of_columns = ['fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount', 'congestion_surcharge', 'ehail_fee']
    for column in rest_of_columns:
        if column in df.columns:
            df[column] = df[column].astype(float64)

    if 'trip_type' in df.columns:
        print(f"pre: missing trip_type count: {df.trip_type.isna().sum()}")
        df.trip_type.fillna(0, inplace=True)
        print(f"post: missing trip_type count: {df.trip_type.isna().sum()}")
        df.trip_type = df.trip_type.astype(int32)
    
    return df

@flow(name="transformation-orchestrator")
def transformation_orchestrator(df):
    df_cleaned = clean_taxi_data(df)
    return df_cleaned