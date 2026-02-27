from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.remote(cluster_id="0227-093001-xxb1s9hc").getOrCreate()
spark.sql("SELECT 1").show()
