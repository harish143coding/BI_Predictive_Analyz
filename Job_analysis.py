"""
to create an analysis over the applying positions
step 1: create a db and load the existing data into the db
step 2 : fetch this data from the db to find KPIs

"""
from sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import pyodbc

positions_df = pd.read_excel(io="../applications-flow.xlsx")

positions_df.shape
positions_df.head

# pandas remaining columns
positions_df.rename(mapper={"Date": "date of apply", "Position": "Job_role",
                            "company": "company", "Link": "details", "Response": "response"},
                    axis='columns',
                    inplace=True)

# original dataframe is modified by removing the null columns
modified_df = positions_df.loc[:, 'date of apply': 'response']
print(modified_df.describe())

# insert this dataframe into a table by creating a new table in MS SQL server.
# -- creating the engine to connect to the database
url_object = URL.create(
    "mssql+pyodbc",
    username="DESKTOP-PT5IK6F/harish",
    host="DESKTOP-PT5IK6F",
    database="sampledb"
     )
# creating engine string in the following method 1
engine_1 = create_engine(url_object)

# creating engine string in the following method 2
engine_2 = create_engine("mssql+pyodbc://harish:@DESKTOP-PT5IK6F/sampledb",
                         pool_pre_ping= True
                        )
# other variant using pyodbc
engine_3 = pyodbc.connect('Driver = {ODBC Driver 17 for SQL Server};Server=DESKTOP-PT5IK6F;'
                            'Database=sampledb;Trusted_Connection=yes;')

# Check the connection
#with engine_3.connect() as connection:
    #print("Connection successful!")