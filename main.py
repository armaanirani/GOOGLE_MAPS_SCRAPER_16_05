import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SEARCH_QUERY = "Architecture firms Pune, Maharashtra"


def scrape_google_maps_data(pages=1, results_per_page=20):
    url = "https://google.serper.dev/maps"
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "q": SEARCH_QUERY,
        "hl": "en", # Language (e.g., "en" for English)
        "gl": "in", # Country code (e.g., "us" for USA)
    }
    
    response = requests.post(url, headers=headers, json=payload)
    # print(response.json())
    data = response.json()
    
    # Extracting the business data
    businesses = []
    if "places" in data:
        for place in data["places"]:
            business = {
                "name": place.get("title"),
                "address": place.get("address"),
                "Phone": place.get("phoneNumber"),
                "rating": place.get("rating"),
                "website": place.get("website")
            }
            businesses.append(business)

    return businesses

# Running the scraper
business_data = scrape_google_maps_data()

# Saving to an excel file
df = pd.DataFrame(business_data)
df.to_excel(f"{SEARCH_QUERY}_data.xlsx", index=False)