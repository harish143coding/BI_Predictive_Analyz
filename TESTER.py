from data_analyze import df
from data_analyze import parse_company_info
from data_analyze import db_engine
import pandas as pd

query = "SELECT * FROM Apply"
df = pd.read_sql('Apply', db_engine)

df[['Company_URL', 'Location_URL']] = df['details'].apply(lambda x: pd.Series(parse_company_info(x)))

df.head()
