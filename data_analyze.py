# here fetch the data from the database and perform analysis using Pandas, D-Tale
from bs4 import BeautifulSoup
from config import DB_CONFIG
from sqlalchemy import create_engine
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
    if pd.isna(company_name) or company_name.strip() == "":
        return "Company name missing"
    search_url = f"https://en.wikipedia.org/wiki/{company_name.replace(' ', '_')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the infobox and search for location information
    try:
        infobox = soup.find('table', {'class': 'infobox vcard'})
        location = infobox.find('td', {'class': 'label'}, text='Headquarters').find_next_sibling('td').text.strip()
        return location
    except AttributeError:
        return "Location not found"

# Apply the function to get company locations using the company name
#df['Location'] = df['company'].apply(get_company_location)

# Trying to find the company from the job URL information
def parse_company_info(url):
    if pd.isna(url) or url.strip() == "":
        return "URL missing", "URL missing"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example for 'indeed.com'
        if "indeed.com" in url:
            try:
                company_name = soup.find('div', {'class': 'icl-u-lg-mr--sm icl-u-xs-mr--xs'}).text.strip()
                location = soup.find('div', {'class': 'jobsearch-InlineCompanyRating'}).find_next_sibling(
                    'div').text.strip()
                return company_name, location
            except AttributeError:
                return "Company name not found", "Location not found"

        # Example for 'glassdoor.com'
        elif "glassdoor.com" in url:
            try:
                company_name = soup.find('div', {'class': 'css-16nw49e e11nt52q1'}).text.strip()
                location = soup.find('div', {'class': 'css-56kyx5 e1tk4kwz5'}).text.strip()
                return company_name, location
            except AttributeError:
                return "Company name not found", "Location not found"

        # Default case for unknown structures
        else:
            return "Unknown structure", "Unknown structure"

    except requests.exceptions.RequestException:
        return "Error accessing URL", "Error accessing URL"


# Apply the function to parse company info
df[['Company_URL', 'Location_URL']] = df['details'].apply(lambda x: pd.Series(parse_company_info(x)))

print(df)

print(df.head())
print(df.info())
#print(df['Location'].nunique())
# implement the above function and check... shoud be worked on further.