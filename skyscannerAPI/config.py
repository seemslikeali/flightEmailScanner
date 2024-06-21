import requests
import os
from dotenv import load_dotenv
# Define the RapidAPI headers

load_dotenv()

headers = {
    "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com",
    "Content-Type": "application/json"
}

def get_skyscanner_config():
    """
    Retrieve the Skyscanner configuration and filter for Canada.
    """
    url = "https://sky-scanner3.p.rapidapi.com/get-config"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            config_data = response.json()['data']
            # Filter for Canada (entry with index 34)
            canada_config = config_data[34]
            return canada_config
        else:
            raise Exception(f"Failed to get configuration: {response.status_code}")
    except Exception as e:
        raise Exception(f"Failed to retrieve Skyscanner configuration: {e}")

if __name__ == "__main__":
    try:
        canada_config = get_skyscanner_config()
        print("Canada Configuration:")
        print(canada_config)
    except Exception as e:
        print(f"An error occurred: {e}")