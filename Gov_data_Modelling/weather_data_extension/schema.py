import pandas as pd
from weather_dwh import temperature_df, rainfall_df, aqi_df


def create_time_dimension(start_date, end_date):
    """
    Create a time dimension DataFrame with one row per day between start_date and end_date.
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    time_dim = pd.DataFrame({'FullDate': dates})

    # Create surrogate key in the format YYYYMMDD
    time_dim['DateKey'] = time_dim['FullDate'].dt.strftime('%Y%m%d').astype(int)
    time_dim['Day'] = time_dim['FullDate'].dt.day
    time_dim['Month'] = time_dim['FullDate'].dt.month
    time_dim['MonthName'] = time_dim['FullDate'].dt.month_name()
    time_dim['Quarter'] = time_dim['FullDate'].dt.quarter
    time_dim['Year'] = time_dim['FullDate'].dt.year
    time_dim['WeekOfYear'] = time_dim['FullDate'].dt.isocalendar().week
    time_dim['DayOfWeek'] = time_dim['FullDate'].dt.day_name()
    time_dim['IsWeekend'] = time_dim['FullDate'].dt.dayofweek >= 5  # Saturday or Sunday

    return time_dim






# Convert AQI and rainfall 'date' columns to datetime.
aqi_df['date'] = pd.to_datetime(aqi_df['date'])
rainfall_df['date'] = pd.to_datetime(rainfall_df['date'])

# For temperature data, build a 'date' column using the first day of the month.
if 'year' in temperature_df.columns and 'month' in temperature_df.columns:
    temperature_df['date'] = pd.to_datetime(
        temperature_df['year'].astype(str) + '-' + temperature_df['month'].astype(str) + '-01'
    )

# Determine overall date range across all datasets.
min_date = min(aqi_df['date'].min(), temperature_df['date'].min(), rainfall_df['date'].min())
max_date = max(aqi_df['date'].max(), temperature_df['date'].max(), rainfall_df['date'].max())

# Create the Time Dimension table.
time_dim = create_time_dimension(min_date, max_date)

# Optional: Display the Time Dimension table
print("Time Dimension Table:")
print(time_dim.head())

# Merge each fact DataFrame with the Time Dimension using the generated 'date' column.
aqi_fact = aqi_df.merge(time_dim, left_on='date', right_on='FullDate', how='left')
temp_fact = temperature_df.merge(time_dim, left_on='date', right_on='FullDate', how='left')
rainfall_fact = rainfall_df.merge(time_dim, left_on='date', right_on='FullDate', how='left')

"""
Nextstep: temperature dataframe months should be arranged properly and then test Time dimension schema
"""