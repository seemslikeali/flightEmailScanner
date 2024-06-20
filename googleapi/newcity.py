import requests

# Define the RapidAPI headers
headers = {
    "x-rapidapi-key": "your_rapidapi_key_here",
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

def search_one_way_flights(from_location, to_location, depart_date):
    """
    Search for one-way flights from a given location to another on a specific date.
    """
    config = get_skyscanner_config()
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"
    params = {
        "fromEntityId": from_location,
        "toEntityId": to_location,
        "departDate": depart_date,
        "market": config['market'],
        "locale": config['locale'],
        "currency": config['currency']
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Flight search failed: {response.status_code}")

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

def find_flights(from_location_name, to_location_name, depart_date):
    """
    Find flights between two locations on a given date.
    """
    from_location_id = auto_complete_query(from_location_name)
    to_location_id = auto_complete_query(to_location_name)
    flights = search_one_way_flights(from_location_id, to_location_id, depart_date)
    return flights

if __name__ == "__main__":
    try:
        from_location = "New York"
        to_location = "Los Angeles"
        depart_date = "2024-07-15"
        flights = find_flights(from_location, to_location, depart_date)
        print(flights)
    except Exception as e:
        print(f"An error occurred: {e}")
