# here fetch the data from the database and perform analysis using Pandas, D-Tale
from sqlalchemy import create_engine
from config import DB_CONFIG
import pandas as pd
import dtale



connection_string = (f'{DB_CONFIG["drivername"]}://{DB_CONFIG["username"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}'
                     f'/{DB_CONFIG["database"]}')

db_engine = create_engine(url=connection_string)

# using pandas fetching the data from a table in the database
query = "SELECT * FROM Apply"
df = pd.read_sql('Apply', db_engine)

# EDA using dtale
dtale.show(df)