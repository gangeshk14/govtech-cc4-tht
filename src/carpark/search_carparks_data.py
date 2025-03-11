import pandas as pd
import json
from rich.prompt import Prompt
from rich.table import Table
from fuzzywuzzy import process
from rich.console import Console
console = Console()
def search_carparks_data_from_cp_num(carparks_data_merged_df, carpark_number):
    """
    Retrieves information for a given carpark number and returns it as a JSON object.

    Args:
        df (pd.DataFrame): The DataFrame containing carpark information.
        carpark_number (str): The carpark number to retrieve information for.

    Returns:
        str: A JSON string containing the carpark information, or None if the carpark number is not found.
    """
    carpark_data = carparks_data_merged_df[carparks_data_merged_df['carpark_number'] == carpark_number]
    if carpark_data.empty:  
        return "Carpark Number does not exist"
    
    result = {
        "update_time":carpark_data['update_datetime'].iloc[0],
        "total_lots": {},
        "lots_available": {},
        "lot_types": list(carpark_data['lot_type'].unique()),
        "type_of_parking_system": carpark_data['type_of_parking_system'].iloc[0],
        "short_term_parking": carpark_data['short_term_parking'].iloc[0],
        "night_parking": carpark_data['night_parking'].iloc[0],
        "free_parking": carpark_data['free_parking'].iloc[0],
        "x_coord": carpark_data['x_coord'].iloc[0],
        "y_coord": carpark_data['y_coord'].iloc[0],
        "address": carpark_data['address'].iloc[0]
    }

    for index, row in carpark_data.iterrows():
        lot_type = row['lot_type']
        result["total_lots"][lot_type] = row['total_lots']
        result["lots_available"][lot_type] = row['lots_available']

    return json.dumps(result, indent=4)
def search_carparks_data_from_address(carparks_data_merged_df, address):
    """
    Retrieves information for a given carpark number and returns it as a JSON object.

    Args:
        df (pd.DataFrame): The DataFrame containing carpark information.
        carpark_number (str): The carpark number to retrieve information for.

    Returns:
        str: A JSON string containing the carpark information, or None if the carpark number is not found.
    """
    carpark_data = carparks_data_merged_df[carparks_data_merged_df['address'] == address]
    if carpark_data.empty:  
        return "Address does not exist"

    result = {
        "update_time":carpark_data['update_datetime'].iloc[0],
        "total_lots": {},
        "lots_available": {},
        "lot_types": list(carpark_data['lot_type'].unique()),
        "type_of_parking_system": carpark_data['type_of_parking_system'].iloc[0],
        "short_term_parking": carpark_data['short_term_parking'].iloc[0],
        "night_parking": carpark_data['night_parking'].iloc[0],
        "free_parking": carpark_data['free_parking'].iloc[0],
        "x_coord": carpark_data['x_coord'].iloc[0],
        "y_coord": carpark_data['y_coord'].iloc[0],
        "address": carpark_data['address'].iloc[0]
    }

    for index, row in carpark_data.iterrows():
        lot_type = row['lot_type']
        result["total_lots"][lot_type] = row['total_lots']
        result["lots_available"][lot_type] = row['lots_available']

    return json.dumps(result, indent=4)

def suggest_addresses(addresses, address):
    """Find the best matching address and return carpark details."""
    
    while True:
        # Get top 5 closest matches
        matches = process.extract(address, addresses, limit=5)
        print(matches)
        # Create a table for better display
        table = Table(title="Did you mean one of these addresses?", show_header=True, header_style="bold magenta")
        table.add_column("Index", justify="center")
        table.add_column("Address", justify="left")

        for i, (match, score, idx) in enumerate(matches, 1):
            table.add_row(str(i), match)

        console.print(table)

        # Let user select or enter a new query
        choice = Prompt.ask("[bold yellow]Enter the number of the correct address (or type again, 'exit' to quit)[/bold yellow]")

        if choice.lower() in ["exit"]:
            console.print("[bold red]Exiting search.[/bold red]")
            return None  # Indicate that the user exited

        if choice.isdigit() and 1 <= int(choice) <= len(matches):
            selected_address = matches[int(choice) - 1][0]
            return selected_address
            break  # Exit loop once a valid selection is made
        else:
            console.print("[bold yellow]Invalid choice. Please try again or type 'q' to exit.[/bold yellow]")
            address = choice  # Update address and re-run matching