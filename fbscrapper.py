from helium import *
import time

def start_browser():
    # Start Chrome and open FlightHub
    start_chrome('google.com')
    write('flighthub.com/#flights')
    press(ENTER)
    click('Cheap Flights - FlightHub.com')

def set_trip(departure_city, destination_city, departure_date, return_date):
    # Click on the 'From' input field and enter the departure city
    click("From")
    write(departure_city, into="From")

    # Click on the 'To' input field and enter the destination city
    click("To")
    write(destination_city, into="To")

    # Click on the departure date field
    click("Depart")
    # Wait briefly for the calendar to load (adjust as needed)
    time.sleep(2)
    # Select the departure date from the calendar
    click(departure_date)

    # Click on the return date field
    click("Return")
    # Wait briefly for the calendar to load (adjust as needed)
    time.sleep(2)
    # Select the return date from the calendar
    click(return_date)

    # Click the search button
    click("Search Flights")

    # Wait for a few seconds to let the results load (adjust time as necessary)
    time.sleep(10)

# Example usage:
browser = start_browser()
set_trip("New York", "Los Angeles", "07/10/2024", "07/17/2024")

# Close the browser after the task is done
browser.quit()