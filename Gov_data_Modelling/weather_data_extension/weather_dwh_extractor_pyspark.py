"""
extracting from the sources using the pyspark library
"""

from pyspark.sql import SparkSession, functions as F, types as T

# Initialize SparkSession
spark = SparkSession.builder.appName("TemperatureDataProcessing").getOrCreate()


def get_temperature_data(source_file, state_weights):
    """
    This function takes the raw temperature data from the OGoV portal and computes the mean temperature monthly, state-wise,
    from 1901 to 2021. It returns a Spark DataFrame with adjusted mean temperature data.

    Parameters:
      - source_file: path to the CSV file.
      - state_weights: dictionary mapping state names to their weight (e.g., {"State1": 0.8, "State2": 1.2, ...})

    Returns:
      Spark DataFrame with columns: state_name, YEAR, mean_temperature_JAN, ..., mean_temperature_DEC, mean_temperature_annual
    """
    # Read CSV file with header and infer schema if possible.
    df = spark.read.csv(source_file, header=True, inferSchema=True)

    # Drop columns not needed.
    df = df.drop("JAN-FEB", "MAR-MAY", "JUN-SEP", "OCT-DEC")

    # List of month columns.
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    # Convert monthly columns and the ANNUAL column to double and replace non-numeric values with 0.
    for m in months:
        df = df.withColumn(m, F.when(F.col(m).cast("double").isNotNull(), F.col(m).cast("double"))
                           .otherwise(F.lit(0.0)))
    df = df.withColumn("ANNUAL", F.when(F.col("ANNUAL").cast("double").isNotNull(), F.col("ANNUAL").cast("double"))
                       .otherwise(F.lit(0.0)))

    # Group by YEAR and calculate the mean for each month and the annual column.
    agg_exprs = [F.avg(m).alias(m) for m in months] + [F.avg("ANNUAL").alias("ANNUAL")]
    agg_df = df.groupBy("YEAR").agg(*agg_exprs)

    # Convert state_weights dictionary to a Spark DataFrame.
    # Ensure weights are numeric.
    state_weights_list = [(state, float(weight)) for state, weight in state_weights.items()]
    state_weights_schema = T.StructType([
        T.StructField("state_name", T.StringType(), True),
        T.StructField("weight", T.DoubleType(), True)
    ])
    state_weights_df = spark.createDataFrame(state_weights_list, schema=state_weights_schema)

    # Cross join the state weights with the aggregated temperature data to compute state-specific adjustments.
    cross_df = state_weights_df.crossJoin(agg_df)

    # For each month, calculate the adjusted mean temperature using the state weight.
    for m in months:
        cross_df = cross_df.withColumn("mean_temperature_" + m, F.col("weight") * F.col(m))

    # Calculate the adjusted annual mean temperature.
    cross_df = cross_df.withColumn("mean_temperature_annual", F.col("weight") * F.col("ANNUAL"))

    # Select the final set of columns.
    select_cols = ["state_name", "YEAR"] + ["mean_temperature_" + m for m in months] + ["mean_temperature_annual"]
    result_df = cross_df.select(*select_cols)

    return result_df



# Testin the 1st func with

sampe_df = get_temperature_data("TEMP_ANNUAL_MEAN_1901-2021.csv")
print(sampe_df.head())

"""
Next steps : JAVA should be installed follow chatgpt command
testing the Spark code, should supply the weights and compare with pandas extractor
--> reading/validation done
check this error
  raise PySparkRuntimeError(
pyspark.errors.exceptions.base.PySparkRuntimeError: [JAVA_GATEWAY_EXITED] Java gateway process exited before sending its port number.

4. Run PySpark in Standalone Mode
Before running your script, try initializing PySpark manually:

Ah, there it is — the root cause: Java is not installed or not properly added to your system's PATH.
"""