# test_citibike_utils.py

from datetime import datetime
from src.citibike.citibike_utils import get_trip_duration_mins


def test_get_trip_duration_mins(spark):

    # Create test data programmatically (works with both local PySpark and Databricks Connect)
    test_data = [
        (datetime(2025, 4, 10, 10, 0, 0), datetime(2025, 4, 10, 10, 10, 0), 10),
        (datetime(2025, 4, 10, 10, 0, 0), datetime(2025, 4, 10, 10, 30, 0), 30),
    ]
    schema = "start_timestamp timestamp, end_timestamp timestamp, expected_trip_duration_mins int"
    df = spark.createDataFrame(test_data, schema=schema)

    # Apply the function to calculate trip duration in minutes
    result_df = get_trip_duration_mins(spark, df, "start_timestamp", "end_timestamp", "trip_duration_mins")

    # Collect the results for assertions
    results = result_df.select("trip_duration_mins", "expected_trip_duration_mins").collect()

    # Assert that the differences are as expected
    assert results[0]["trip_duration_mins"] == results[0]["expected_trip_duration_mins"]
    assert results[1]["trip_duration_mins"] == results[1]["expected_trip_duration_mins"]
