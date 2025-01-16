"""
the idea is to carry-out appropriate visualization preferably Geo-Visualization if no the other
Dataset (Gross State Domestic Product): https://www.data.gov.in/resource/gross-state-domestic-product-gsdp-current-prices-states-and-uts-2011-12-2021-22
"""
from OGovD_analysis.config import API_INFO
import requests


gsdp_url = "https://api.data.gov.in/resource/adb4b1da-159f-46b3-a9c0-0545fe9ddda0?"

params = {
    "api-key": API_INFO["api_key"],
    "format": "json",
    "limit": 10000
}

response = requests.get(gsdp_url, params=params)
data = response.json()
print(data["total"])





"""
Next steps:
work on the import error from Chat* soutions
"""