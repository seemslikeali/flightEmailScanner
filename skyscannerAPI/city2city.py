import requests

# Define the RapidAPI headers
headers = {
    "x-rapidapi-key": "e9f71cad4fmsh735a5efce8032dbp14a0dbjsn55332701aad1",
    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com",
    "Content-Type": "application/json"
}

def get_skyscanner_config():
    """
    Retrieve the Skyscanner configuration including market and locale.
    """
    url = "https://sky-scanner3.p.rapidapi.com/get-config"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"Failed to get configuration: {response.status_code}")

if __name__ == "__main__":
    try:
        config = get_skyscanner_config()
        print(config)
    except Exception as e:
        print(f"An error occurred: {e}")
