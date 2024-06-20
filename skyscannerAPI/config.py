import requests
import os
import json
from dotenv import load_dotenv
# Define the RapidAPI headers

load_dotenv()

headers = {
    "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com",
    "Content-Type": "application/json"
}

config_file_path = "canada_config.json"

def get_skyscanner_config():
    """
    Retrieve the Skyscanner configuration and filter for Canada.
    """
    url = "https://sky-scanner3.p.rapidapi.com/get-config"
    print("Sent call")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            config_data = response.json()['data']
            # Filter for Canada (entry with index 35)
            canada_config = config_data[35]
            return canada_config
        else:
            raise Exception(f"Failed to get configuration: {response.status_code}")
    except Exception as e:
        raise Exception(f"Failed to retrieve Skyscanner configuration: {e}")

def load_config():
    """
    Load the configuration for Canada from a local file or fetch from API if not present.
    """
    if os.path.exists(config_file_path):
        # Load the config from the local file
        with open(config_file_path, 'r') as file:
            canada_config = json.load(file)
    else:
        # Fetch the config from the API and save it locally
        canada_config = get_skyscanner_config()
        with open(config_file_path, 'w') as file:
            json.dump(canada_config, file, indent=4)
    return canada_config

if __name__ == "__main__":
    try:
        canada_config = load_config()
        print("Canada Configuration:")
        print(canada_config)
    except Exception as e:
        print(f"An error occurred: {e}")