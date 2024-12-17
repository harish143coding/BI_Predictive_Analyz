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


# Create a SELECT query for specific columns
sql_query = text("""
SELECT rf.location_id, _state_ AS Indian_state, district,  avg_rainfall
FROM rainfall_fact rf
JOIN location_dim ld
ON rf.location_id = ld.location_id
WHERE 1=1 AND
_state_ LIKE 'Andhra%'
LIMIT 10  
""")


# Execute the query
result = session.execute(sql_query)
print(type(result))

# Fetch and print results
for row in result:
    print(row)