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
# -- creating the engine to connect to the database; Here sample postgresdb is created using the online platform
# - Clever-cloud
url_object = URL.create(
    "postgresql+psycopg2",
    username="ub2owelyy5qfecopz0ti",
    password="lGIvHaTmAYbziQbWB4vdxMCT5Etnj1",
    host="b1gnq5ieokuldsatwymf-postgresql.services.clever-cloud.com",
    port="50013",
    database="b1gnq5ieokuldsatwymf"
)
# creating engine string in the following method 1
engine_1 = create_engine(url_object)  # this is a postgresql database engine.

# Check the connection
with engine_1.connect() as connection:
    print("Connection successful!")

#  Loading the data from dataframe to database
db_insertion = modified_df.to_sql(
                            name='Apply',
                            con=engine_1
)