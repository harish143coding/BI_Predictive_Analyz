from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# Initialize the geolocator
geolocator = Nominatim(user_agent="company_locator")

def search_company_address(company_name):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--lang=de-DE")

        # Set up the Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Perform the search
        search_url = f"https://www.google.com/search?q={company_name.replace(' ', '+')}+company+address"
        driver.get(search_url)
        time.sleep(3)  # Wait for the page to load

        # Extract address from the search results
        address_elements = driver.find_elements(By.XPATH, "//div[@class='BNeawe deIvCb AP7Wnd']")
        address = address_elements[0].text if address_elements else "Address not found"

        driver.quit()
        return address
    except Exception as e:
        return "Error during web search"

def get_location(company_name):
    address = search_company_address(company_name)
    if "Address not found" in address or "Error" in address:
        return address, None, None

    try:
        location = geolocator.geocode(address)
        if location:
            return location.address, location.latitude, location.longitude
        else:
            return "Geo-coordinates not found", None, None
    except Exception as e:
        return "Error during geocoding", None, None

# Initialize the geolocator
geolocator = Nominatim(user_agent="company_locator")

def get_location_geopy(company_name):
    try:
        location = geolocator.geocode(company_name)
        if location:
            return location.address, location.latitude, location.longitude
        else:
            return "Location not found", None, None
    except Exception as e:
        return "Error", None, None

# Read the from a dictionary object file
data = {"company": ["Lindhorst Gruppe", "Arvato", "Emsys", "Siemens", "EWE Netz"]}
df = pd.DataFrame.from_dict(data)

# Create new columns for address and coordinates
df[['Address', 'Latitude', 'Longitude']] = df['company'].apply(lambda x: pd.Series(get_location_geopy(x)))


# Save the results to a new CSV file
print("Process completed ", df)

