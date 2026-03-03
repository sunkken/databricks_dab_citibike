"""Configure pytest for local PySpark testing."""

import pytest
import os
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())


@pytest.fixture(scope="session")
def spark():
    """Provide a SparkSession fixture - Databricks Connect if available, else local PySpark."""
    spark = None

    try:
        from databricks.connect import DatabricksSession

        spark = DatabricksSession.builder.getOrCreate()
        print("Using Databricks Connect session")
    except ImportError:
        try:
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName("local-tests").master("local[*]").getOrCreate()
            print("Using local PySpark session")
        except ImportError as exc:
            raise RuntimeError(
                "Neither Databricks Connect nor PySpark is available. Activate a compatible environment."
            ) from exc

    yield spark
    spark.stop()
