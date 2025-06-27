"""imports list"""
from datetime import datetime
import argparse
import json
import requests
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table


# Instead of using print(), you should use the Console from Rich instead.
console = Console(record=True)


def load_weather_for_location(lat: str, lng: str) -> dict:
    """Given a location, load the current weather for that location"""
    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key=b1b135c5f4c946e2929150647241909&q={lat},{lng}")

    weather_data = response.json()

    dest_weather = {}

    temperature = weather_data["current"]["temp_c"]
    dest_weather["Temp"] = temperature
    weather = weather_data["current"]["condition"]["text"]
    dest_weather["Weather"] = weather

    return dest_weather


def render_flights(flights: list) -> None:
    """Render a list of flights to the console using the Rich Library

    Consider using Panels, Grids, Tables or any of the more advanced
    features of the library"""

    console.print(flights)


def get_flights_from_iata(iata: str) -> list:
    """Given an IATA get the flights that are departing from that airport from Airlabs"""
    response = requests.get(
        f"https://airlabs.co/api/v9/schedules?dep_iata={iata}&api_key=0dc0ae5d-18fd-4265-907a-f384fef6d1a9")
    api_airport_data = response.json()
    flights_details = api_airport_data["response"]

    return flights_details


def load_airport_json() -> list[dict]:
    """Returns airport information loaded from a file."""
    with open("airports.json") as f:
        data = json.load(f)
    return data


def find_airports_from_name(name: str, airport_data: list) -> list:
    """
    Find an airport from the airport_data given a name
    Could return one or more airport objects
    """
    possible_choices = []
    airport_list = []
    for airport in airport_data:
        if isinstance(airport["name"], str):
            if airport["name"] == name:
                airport_list.append(airport)
                return airport_list
            if name in airport["name"]:
                possible_choices.append(airport)
    return possible_choices


def multiple_airports_choice(choices_list: list[dict]) -> str:
    """Returns list of airports for user to choose from"""
    choice_names = []
    for i in choices_list:
        choice_names.append(i["name"])

    airport = Prompt.ask(
        "Multiple airports found, please choose one: ", choices=choice_names)
    return airport


def find_airport_from_iata(to_be_found_iata: str, airport_json_data: list[dict]) -> dict:
    """
    Find an airport from the airport_data given a name
    Should return exactly one airport object
    """
    for airport in airport_json_data:
        if airport["iata"] == to_be_found_iata:
            return airport["name"]


def find_airport_lat(to_be_found_iata: str, airport_json_data: list[dict]) -> dict:
    """
    Find an airport from the airport_data given a name
    Should return latitude
    """
    for airport in airport_json_data:
        if airport["iata"] == to_be_found_iata:
            return airport["lat"]


def find_airport_lon(to_be_found_iata: str, airport_json_data: list[dict]) -> dict:
    """
    Find an airport from the airport_data given a name
    Should return longitude
    """
    for airport in airport_json_data:
        if airport["iata"] == to_be_found_iata:
            return airport["lon"]


def ask_for_airport_name():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--airport")
    parser.add_argument("--export", choices=["html", "json"])
    args = parser.parse_args()

    export_format = args.export
    if not export_format:
        print("No export format chosen. Defaulting to HTML export")
        export_format = "html"
    elif export_format not in ["html", "json"]:
        raise ValueError("Has to be HTML or JSON")

    airport_name = args.airport
    if airport_name == "":
        airport_name = input("Enter an airport: ")
    return airport_name, export_format


def find_airport(airport_data, airport_name):
    """Returns airport from user's input"""
    airports_found = find_airports_from_name(airport_name, airport_data)

    if not airports_found:
        raise ValueError("Not in data")

    if len(airports_found) > 1:
        new_airport_name = multiple_airports_choice(airports_found)
        airports_found = find_airports_from_name(
            new_airport_name, airports_found)

    return airports_found


def get_flights_details(airport_data, api_flights_data):
    """Returns all flights details for a particular airport"""
    arr_iata_all_flights = []

    all_flights_details = []

    for flight in api_flights_data:
        flight_dict = {}
        arr_iata = flight["arr_iata"]
        arr_iata_all_flights.append(arr_iata)

        flight_number = flight["flight_number"]
        flight_dict["flight_number"] = flight_number

        dep_time = flight["dep_time"]
        flight_dict["dep_time"] = dep_time

        airport_name = find_airport_from_iata(arr_iata, airport_data)
        flight_dict["destination airport"] = airport_name

        lat = find_airport_lat(arr_iata, airport_data)
        lon = find_airport_lon(arr_iata, airport_data)
        dest_weather = load_weather_for_location(lat, lon)
        temp = dest_weather["Temp"]
        flight_dict["Temp"] = str(temp)
        weather = dest_weather["Weather"]
        flight_dict["Weather"] = weather

        all_flights_details.append(flight_dict)
    return all_flights_details


def create_table_flight_details(all_flights_details: list[dict]):
    """Creates table for the flight details"""
    table = Table(title="Flights")
    table.add_column("Flight number", style="cyan")
    table.add_column("Dept. Time", style="cyan")
    table.add_column("Destination", style="cyan")
    table.add_column("Weather", style="cyan")
    table.add_column("Temp.", style="cyan")

    for flight_details in all_flights_details:
        table.add_row(flight_details["flight_number"],
                      flight_details["dep_time"], flight_details["destination airport"], flight_details["Weather"], flight_details["Temp"])
    return table


def export_to_json(flight_data: list, filename: str) -> None:
    """Exporting flight data to JSON"""
    with open(filename, "w") as json_file:
        json.dump(flight_data, json_file, indent=4)

    print(f"Flight details exported to {filename}")


if __name__ == "__main__":

    airport_data = load_airport_json()

    airport_name, export_format = ask_for_airport_name()
    print(f"Airport: {airport_name}")
    print(f"Export format: {export_format}")

    airports_found = find_airport(airport_data, airport_name)

    iata_code = airports_found[0]["iata"]
    print(f"Departure iata code: {iata_code}")

    api_flights_data = get_flights_from_iata(iata_code)

    all_flights_details = get_flights_details(airport_data, api_flights_data)

    table_flight_details = create_table_flight_details(all_flights_details)

    console.print(table_flight_details)

    # Generate a unique filename using the current date and time
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    html_filename = f"flight_details_{timestamp}.html"
    json_filename = f"flight_details_{timestamp}.json"

    # Export the data based on chosen format
    if export_format == "html":
        console.save_html(html_filename)
        console.print(f"Flight details exported to {html_filename}")
    elif export_format == "json":
        export_to_json(all_flights_details, json_filename)
