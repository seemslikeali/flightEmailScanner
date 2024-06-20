import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define the RapidAPI headers
headers = {
    "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),  # API key loaded from environment variables
    'x-rapidapi-host': "sky-scanner3.p.rapidapi.com",  # API host for Skyscanner
    'X-RapidAPI-Mock-Response': "200"  # Optional mock response header for testing
}

def autocomplete_location(city, country):
    """
    Get auto-complete suggestions for airports given a city and country.

    Parameters:
    city (str): The name of the city for which to get auto-complete suggestions.
    country (str): The name of the country to refine the search.

    Returns:
    list: A list of suggestions returned by the Skyscanner API.

    Raises:
    Exception: If there is an issue with the API request.
    """
    # API endpoint for auto-complete
    url = "https://sky-scanner3.p.rapidapi.com/auto-complete"
    # Construct query parameters to include both city and country for better accuracy
    query = {"query": f"{city}, {country}"}

    try:
        # Send GET request to the Skyscanner API with headers and query parameters
        response = requests.get(url, headers=headers, params=query)
        # Check if the response status code indicates success
        if response.status_code == 200:
            # Parse the JSON response and extract the 'data' field
            suggestions = response.json()['data']
            return suggestions
        else:
            # Raise an exception if the API request failed
            raise Exception(f"Failed to get auto-complete suggestions: {response.status_code}")
    except Exception as e:
        # Raise an exception if there was an issue with the request
        raise Exception(f"Failed to retrieve auto-complete suggestions: {e}")

if __name__ == "__main__":
    # Prompt the user to enter a city
    city = input("Enter city: ")
    # Prompt the user to enter a country
    country = input("Enter country: ")

    try:
        # Call the autocomplete_location function to get suggestions
        suggestions = autocomplete_location(city, country)
        # Print the auto-complete suggestions in a formatted JSON output
        print("Auto-complete Suggestions:")
        print(json.dumps(suggestions, indent=4))
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"An error occurred: {e}")
