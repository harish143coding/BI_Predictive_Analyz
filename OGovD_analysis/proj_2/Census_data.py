"""
Analysis and visualization
idea to analyze census data from AP, Visakhapatnam
Link: https://ap.data.gov.in/resource/villagetown-wise-primary-census-abstract-2011-visakhapatnam-district-andhra-pradesh

"""
import requests
import pandas as pd
from config import API_INFO

census_url = "https://api.data.gov.in/resource/7360817d-7c02-4e0d-9143-976741df656e?"

params = {
    "api-key": API_INFO["api_key"]
}


"""
next steps:
retrieve the data from this API and make data understanding
"""

