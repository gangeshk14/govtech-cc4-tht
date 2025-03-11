import os
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
import re
#carpark modules
from carpark.get_carparks_data import get_carparks_data
from carpark.search_carparks_data import search_carparks_data_from_cp_num,search_carparks_data_from_address,suggest_addresses

#restaurant modules
from restaurant.restaurant_details import zomato_restaurant_countries_events_to_df,zomato_restaurant_details_to_csv
from restaurant.restaurant_events import extract_restaurant_events_by_mm_yyyy
from restaurant.restaurant_analysis import rating_text_thresholds_analyser
console = Console()
#load env
load_dotenv()

#restaurant scenario constants
RESTAURANT_DETAILS_MAP = {"id":"restaurant_id",
                            "name":"restaurant_name",
                            "Country":"country",
                            "location.city":"city",
                            "user_rating.votes":"user_rating_voted",
                            "user_rating.aggregate_rating":"user_aggregate_rating",
                            "cuisines":"cuisines",
                            "zomato_events":"event_date"
}
RESTAURANTS_EVENT_MAP = {"event_id":"event_id",
                         "id":"restaurant_id",
                         "name":"restaurant_name",
                         "photos":"photo_url",
                        "title":"event_title",
                        "start_date":"event_start_date",
                        "end_date":"event_end_date"

}
RATING_TEXT_LIST = ['Poor','Average', 'Good', 'Very Good', 'Excellent']
MIN_MAX_RATING = (0,5) #assume we have this info
DATA_FOLDER_DIR = os.getenv("DATA_FOLDER_DIR")
DATA_FOLDER_DIR = "../data"
RESTAURANT_JSON_URL="https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
RESTAURANT_DETAILS_FILENAME = "restaurant_details.csv"
RESTAURANT_EVENTS_FILENAME = "restaurant_events.csv"
COUNTRY_CODE_FILENAME = "Country-Code.xlsx"

#carpark scenario constants
DATA_GOV_API_HEAD = "https://api.data.gov.sg/v1"
DATA_GOV_TRANSPORT_API_URL = f"{DATA_GOV_API_HEAD}/transport/carpark-availability"
CARPARK_STATIC_CSV_URL = "https://raw.githubusercontent.com/Papagoat/brain-assessment/refs/heads/main/HDBCarparkInformation.csv"

def get_valid_mm_yyyy_input():
    """Prompts the user for a month and year (mm_yyyy) and validates the input, with a 'back' option."""
    while True:
        mm_yyyy = Prompt.ask("Enter month and year (mm_yyyy), or 'back' to return:")
        if mm_yyyy == "back":
            return None  # Return None to indicate the user wants to go back
        elif re.match(r"^(0[1-9]|1[0-2])_(20\d{2})$", mm_yyyy):  # Validate mm_yyyy format
            return mm_yyyy
        else:
            console.print("[bold red]Invalid format. Please enter mm_yyyy (e.g., 01_2024), or 'back'.[/bold red]")

#runs restaurant scenario in cli
def restaurant_scenario():
    try:
        restaurants_countries_expanded_df = zomato_restaurant_countries_events_to_df(
            RESTAURANT_JSON_URL, DATA_FOLDER_DIR, COUNTRY_CODE_FILENAME, RESTAURANT_DETAILS_MAP
        )
    except Exception as e:
        print(f"Something went wrong...{e}")
        return

    while True:
        choice = Prompt.ask(
            "Choose an option: [bold blue]1[/bold blue] Export restaurant details, [bold blue]2[/bold blue] Extract events, [bold blue]3[/bold blue] Analyze ratings, [bold red]back[/bold red] to home",
            choices=["1", "2", "3", "back"],
        )

        if choice == "1":
            try:
                zomato_restaurant_details_to_csv(
                    restaurants_countries_expanded_df,
                    RESTAURANT_DETAILS_MAP,
                    RESTAURANT_DETAILS_FILENAME,
                    DATA_FOLDER_DIR,
                )
            except Exception as e:
                print(f"Something went wrong...{e}")
        elif choice == "2":
            event_mm_yyyy = get_valid_mm_yyyy_input()
            if event_mm_yyyy is None:  # User chose to go back
                continue  # Go back to the scenario menu
            try:
                extract_restaurant_events_by_mm_yyyy(
                    event_mm_yyyy,
                    restaurants_countries_expanded_df,
                    DATA_FOLDER_DIR,
                    RESTAURANTS_EVENT_MAP,
                    RESTAURANT_EVENTS_FILENAME,
                )
            except Exception as e:
                print(f"Something went wrong...{e}")
        elif choice == "3":
            try:
                rating_text_thresholds_analyser(
                    restaurants_countries_expanded_df, RATING_TEXT_LIST, MIN_MAX_RATING
                )
            except Exception as e:
                print(f"Something went wrong...{e}")
        elif choice == "back":
            return
#runs carpark scenario in cli
def carpark_scenario():
    try:
        carparks_data_merged_df = get_carparks_data(DATA_GOV_TRANSPORT_API_URL, CARPARK_STATIC_CSV_URL)
    except Exception as e:
        print(f"Something went wrong...{e}")
        return

    while True:
        choice = Prompt.ask(
            "Query by [bold blue]1[/bold blue] Carpark Number, [bold blue]2[/bold blue] Address, or [bold red]back[/bold red] to home?",
            choices=["1", "2", "back"],
        )

        if choice == "1":
            cp_num = Prompt.ask("Enter Carpark Number (eg 'AM64')")
            returned = search_carparks_data_from_cp_num(carparks_data_merged_df, cp_num)
            console.print(returned)

        elif choice == "2":
            address = Prompt.ask("Enter Address (partial or full) eg. Bishan")
            addresses = carparks_data_merged_df["address"]
            chosen_address = suggest_addresses(addresses,address)
            if chosen_address:
                returned = search_carparks_data_from_address(carparks_data_merged_df, chosen_address)
                console.print(returned)

        elif choice == "back":
            return
def main():
    while True:
        choice = Prompt.ask(
            "Choose a scenario: [bold blue]1[/bold blue] Restaurant, [bold blue]2[/bold blue] Carpark, or [bold red]exit[/bold red]?",
            choices=["1", "2", "exit"],
        )
        if choice == "1":
            restaurant_scenario()
        elif choice == "2":
            carpark_scenario()
        elif choice == "exit":
            console.print("[bold green]Exiting program.[/bold green]")
            break

if __name__ == "__main__":
    main()
        
