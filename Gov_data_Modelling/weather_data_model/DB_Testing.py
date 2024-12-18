from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from config import DB_CONFIG

# Database credentials and connection
# DB Parameters
db_type = 'postgresql'  # or 'postgresql', 'sqlite', etc.
db_user = DB_CONFIG["username"]
db_password = DB_CONFIG["password"]
db_host = DB_CONFIG['host']
db_port = DB_CONFIG["port"]
db_name = DB_CONFIG["database"]

db_url = f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the existing database schema
metadata = MetaData()
table_name = 'location_dim'  # Replace with your table name
table = Table(table_name, metadata, autoload_with=engine)

# Fetch and print results
def get_query(query):
    """
    input a query to the fn it queries the DB and gives the output
    """
    result = session.execute(query)
    for row in result:
        print(row)

# Testing the function with sample queries
#query 1
sql_query_1 = text("""
SELECT rf.location_id, _state_ AS Indian_state, district,  avg_rainfall
FROM rainfall_fact rf
JOIN location_dim ld
ON rf.location_id = ld.location_id
WHERE 1=1 AND
_state_ LIKE 'Andhra%'
LIMIT 10  
""")

sql_query_2 = text("""
SELECT time_id, MAX(year), MAX(month)
FROM time_dim td
GROUP BY time_id
ORDER BY time_id
""")

#TESTING
get_query(sql_query_2)