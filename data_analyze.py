# here fetch the data from the database and perform analysis using Pandas, D-Tale
from sqlalchemy import create_engine
from config import DB_CONFIG
import pandas as pd
import requests



connection_string = (f'{DB_CONFIG["drivername"]}://{DB_CONFIG["username"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}'
                     f'/{DB_CONFIG["database"]}')

db_engine = create_engine(url=connection_string)

# using pandas fetching the data from a table in the database
query = "SELECT * FROM Apply"
df = pd.read_sql('Apply', db_engine)


# Data Cleaning/Enhancing: improve the quality of the data in the frame
# replacing the 'None' values in between the timestamps with preceding time stamp.
df['date of apply'].fillna('ffill')

# finding the company location and adding that to new column


def get_company_location(company_name):
    url = "https://search.infobelpro.com/germany/en/api/search"
    headers = {"Content-Type": "application/json"}
    payload = {"company_name": company_name}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["location"]
    else:
        return "Location not found"


df['Location_1'] = df['company'].apply(get_company_location)
print(df.head())
print(df.info())
# implement the above function and check... shoud be worked on further.