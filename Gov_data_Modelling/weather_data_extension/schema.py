import pandas as pd


def create_time_dimension(start_date, end_date):
    """
    Create a time dimension DataFrame with one row per day between start_date and end_date.
    """
    # Generate a date range with daily frequency.
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    time_dim = pd.DataFrame({'FullDate': dates})

    # Create a surrogate key in the format YYYYMMDD (as integer)
    time_dim['DateKey'] = time_dim['FullDate'].dt.strftime('%Y%m%d').astype(int)
    time_dim['Day'] = time_dim['FullDate'].dt.day
    time_dim['Month'] = time_dim['FullDate'].dt.month
    time_dim['MonthName'] = time_dim['FullDate'].dt.month_name()
    time_dim['Quarter'] = time_dim['FullDate'].dt.quarter
    time_dim['Year'] = time_dim['FullDate'].dt.year
    time_dim['WeekOfYear'] = time_dim['FullDate'].dt.isocalendar().week
    time_dim['DayOfWeek'] = time_dim['FullDate'].dt.day_name()
    time_dim['IsWeekend'] = time_dim['FullDate'].dt.dayofweek >= 5  # True if Saturday (5) or Sunday (6)

    return time_dim


# Example stubs for your data functions
def get_aqi_data():
    # This should return your AQI data as a DataFrame with a 'date' column and 'aqi' measure.
    # Example:
    data = {
        'date': ['2025-01-01', '2025-01-02', '2025-01-03'],
        'aqi': [45, 50, 47]
    }
    return pd.DataFrame(data)



"""
Nextstep: started with time dimension  GPT follows
"""