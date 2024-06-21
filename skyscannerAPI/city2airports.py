import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the RapidAPI headers
headers = {
    "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
    'x-rapidapi-host': "sky-scanner3.p.rapidapi.com",
}

def get_airports_from_location(query):
    """
    Retrieve the list of airports for a given location query using Skyscanner API.
    """
    url = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"
    querystring = {"query": query}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        airport_data = response.json()
        return airport_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    except Exception as e:
        print(f"Other error occurred: {e}")

def filter_airports_by_country(data, country):
    """
    Filter the JSON data to include only entries that match the specified country.
    """
    filtered_data = {
        "data": [entry for entry in data['data'] if entry['presentation']['subtitle'] == country],
        "status": data.get('status', True),
        "message": data.get('message', "Filtered")
    }
    return filtered_data

def load_or_fetch_city_data(city, country):
    """
    Load the airport data for a city from a local file or fetch from API if not present.
    Filter the data to include only entries that match the specified country.
    """
    city_file_path = f"skyscannerAPI/temp/{country}_{city}.json"
    
    if os.path.exists(city_file_path):
        print(f"Local data for {city} found. Using the local data.")
        with open(city_file_path, 'r') as file:
            city_data = json.load(file)
    else:
        print(f"Local data for {city} not found. Fetching from API.")
        city_data = get_airports_from_location(city)
        if city_data:
            # Filter the city data by country
            filtered_city_data = filter_airports_by_country(city_data, country)
            with open(city_file_path, 'w') as file:
                json.dump(filtered_city_data, file, indent=4)
            city_data = filtered_city_data
        else:
            print(f"Failed to fetch data for {city} from API.")
    return city_data

if __name__ == "__main__":
    # Example city and country query for airport autocomplete
    query_city = "Saskatoon"
    query_country = "Canada"

    try:
        airports = load_or_fetch_city_data(query_city, query_country)
        if airports:
            print(f"Airports for city '{query_city}' in country '{query_country}':")
            print(airports)
        else:
            print(f"No airports data available for city '{query_city}' in country '{query_country}'.")
    except Exception as e:
        print(f"An error occurred while fetching airports: {e}")
