"""
For the Transformation step PySpark library will used, which has the parallel computation ability!
"""

from weather_dwh import temperature_df, rainfall_df, aqi_df

from pyspark.sql import SparkSession, functions as F, types as T

# Initialize SparkSession
spark = SparkSession.builder.appName("WeatherDataWarehouse").getOrCreate()


def create_time_dimension(start_date, end_date):
    """
    Create a time dimension DataFrame with one row per day between start_date and end_date.
    start_date and end_date should be strings in 'yyyy-MM-dd' format.
    """
    # Create a one-row DataFrame with start and end dates.
    df = spark.createDataFrame([(start_date, end_date)], ["start", "end"])

    # Use the sequence function to generate an array of dates and then explode it to create one row per day.
    time_dim = df.select(
        F.explode(F.sequence(F.to_date("start", "yyyy-MM-dd"), F.to_date("end", "yyyy-MM-dd"))).alias("FullDate"))

    # Add additional time attributes.
    time_dim = time_dim.withColumn("DateKey", F.date_format("FullDate", "yyyyMMdd").cast("int")) \
        .withColumn("Day", F.dayofmonth("FullDate")) \
        .withColumn("Month", F.month("FullDate")) \
        .withColumn("MonthName", F.date_format("FullDate", "MMMM")) \
        .withColumn("Quarter", F.quarter("FullDate")) \
        .withColumn("Year", F.year("FullDate")) \
        .withColumn("WeekOfYear", F.weekofyear("FullDate")) \
        .withColumn("DayOfWeek", F.date_format("FullDate", "EEEE")) \
        .withColumn("IsWeekend", F.dayofweek("FullDate").isin(1, 7).cast("boolean"))
    return time_dim




# Retrieve DataFrames for each type of weather data.


# Determine the overall date range across the three datasets.
min_date_aqi = aqi_df.select(F.min("date")).first()[0]
min_date_temp = temperature_df.select(F.min("date")).first()[0]
min_date_rainfall = rainfall_df.select(F.min("date")).first()[0]
max_date_aqi = aqi_df.select(F.max("date")).first()[0]
max_date_temp = temperature_df.select(F.max("date")).first()[0]
max_date_rainfall = rainfall_df.select(F.max("date")).first()[0]

overall_min_date = min(min_date_aqi, min_date_temp, min_date_rainfall)
overall_max_date = max(max_date_aqi, max_date_temp, max_date_rainfall)

# Convert overall_min_date and overall_max_date to strings in "yyyy-MM-dd" format.
overall_min_date_str = overall_min_date.strftime("%Y-%m-%d")
overall_max_date_str = overall_max_date.strftime("%Y-%m-%d")

# Create the Time Dimension DataFrame.
time_dim = create_time_dimension(overall_min_date_str, overall_max_date_str)
time_dim.show(5)

# Join each fact DataFrame with the Time Dimension.
aqi_fact = aqi_df.join(time_dim, aqi_df.date == time_dim.FullDate, "left")
temp_fact = temperature_df.join(time_dim, temperature_df.date == time_dim.FullDate, "left")
rainfall_fact = rainfall_df.join(time_dim, rainfall_df.date == time_dim.FullDate, "left")

# Show the joined DataFrames.
print("AQI Fact Table:")
aqi_fact.show()

print("Temperature Fact Table:")
temp_fact.show()

print("Rainfall Fact Table:")
rainfall_fact.show()

"""
Nextstep: 1. temperature dataframe months should be arranged properly and then test Time dimension schema
Pyspark installed, review the code and go to previous step
"""