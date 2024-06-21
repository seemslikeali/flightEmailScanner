import json
import os

def save_json_locally(data, filename):
    directory = os.path.join('temp', 'flightdata', 'roundtrips')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def display_flight_info(data):
    flights = data['data']['flightQuotes']['results']
    for flight in flights:
        content = flight['content']
        outbound = content['outboundLeg']
        inbound = content['inboundLeg']
        
        print(f"Flight ID: {flight['id']}")
        print(f"Price: {content['price']}")
        print(f"Direct: {'Yes' if content['direct'] else 'No'}")
        print(f"Outbound:")
        print(f"  From: {outbound['originAirport']['name']} ({outbound['originAirport']['skyCode']})")
        print(f"  To: {outbound['destinationAirport']['name']} ({outbound['destinationAirport']['skyCode']})")
        print(f"  Departure Date: {outbound['localDepartureDateLabel']}")
        print(f"Inbound:")
        print(f"  From: {inbound['originAirport']['name']} ({inbound['originAirport']['skyCode']})")
        print(f"  To: {inbound['destinationAirport']['name']} ({inbound['destinationAirport']['skyCode']})")
        print(f"  Departure Date: {inbound['localDepartureDateLabel']}")
        print(f"Trip Duration: {content['tripDuration']}")
        print("\n-----------------------\n")

if __name__ == "__main__":
    # Load the JSON data
    with open('skyscannerAPI/temp/flightdata/roundtrips/flights_data.json', 'r') as f:
        data = json.load(f)
    
    # Save JSON locally
    save_json_locally(data, 'flights_data.json')
    
    # Display flight information
    display_flight_info(data)
