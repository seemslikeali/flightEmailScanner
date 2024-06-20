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

def auto_complete_query(query):
    """
    Get the entityId for a given location name.
    """
    url = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"
    params = {"query": query}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json().get('data', [])
        if results:
            return results[0]['presentation']['id']  # Return the first matching entityId
        else:
            raise Exception("No matching location found")
    else:
        raise Exception(f"Auto-complete query failed: {response.status_code}")


if __name__ == "__main__":
    try:
        location_name = "New York"
        entity_id = auto_complete_query(location_name)
        print(f"Entity ID for {location_name}: {entity_id}")
    except Exception as e:
        print(f"An error occurred: {e}")