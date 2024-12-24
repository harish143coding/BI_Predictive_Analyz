"""
to create an analysis over the applying positions
step 1: create a db and load the existing data into the db
step 2 : fetch this data from the db to find KPIs

"""
import pandas as pd
from sqlalchemy import create_engine, URL
from config import DB_CONFIG
import pyodbc

# Step 1: Read the Excel file into a DataFrame
positions_df = pd.read_excel(io="../applications-flow.xlsx")
print(positions_df.shape)
print(positions_df.head())

# Step 2: Rename columns
positions_df.rename(columns={
    "Date": "date of apply",
    "Position": "Job_role",
    "company": "company",
    "Link": "details",
    "Response": "response"
}, inplace=True)

# Step 3: Filter DataFrame to only include specified columns
modified_df = positions_df.loc[:, 'date of apply':'response']
print(modified_df.describe())

# Step 4: Create a database engine connection string using environment variables or config file
url_object = URL.create(
    drivername=DB_CONFIG["drivername"],
    username=DB_CONFIG["username"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"]
)
engine = create_engine(url_object)

# Step 5: Verify the database connection
with engine.connect() as connection:
    print("Connection successful!")

# Step 6: Load the data from DataFrame to the database table
modified_df.to_sql(name='Apply', con=engine, if_exists='append', index=False)
