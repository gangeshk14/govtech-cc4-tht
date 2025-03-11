from rapidfuzz import process
from carpark.get_carparks_data import get_carparks_data
from carpark.search_carparks_data import search_carparks_data_from_cp_num,search_carparks_data_from_address,suggest_addresses
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
console = Console()
#load env

DATA_GOV_API_HEAD = "https://api.data.gov.sg/v1"
DATA_GOV_TRANSPORT_API_URL = f"{DATA_GOV_API_HEAD}/transport/carpark-availability"
CARPARK_STATIC_CSV_URL = "https://raw.githubusercontent.com/Papagoat/brain-assessment/refs/heads/main/HDBCarparkInformation.csv"
TO_SEARCH = "SB40"
if __name__ == "__main__":
    carparks_data_merged_df = get_carparks_data(DATA_GOV_TRANSPORT_API_URL,CARPARK_STATIC_CSV_URL)
    while True:
        choice = Prompt.ask("Do you want to query by [bold blue]1[/bold blue] Carpark Number, [bold blue]2[/bold blue] Address, or [bold red]exit[/bold red]?", choices=["1", "2", "exit"])

        if choice == "1":
            cp_num = Prompt.ask("Enter Carpark Number")
            returned = search_carparks_data_from_cp_num(carparks_data_merged_df, cp_num)
            console.print(returned)

        elif choice == "2":
            address = Prompt.ask("Enter Address (partial or full)")
            chosen_address = suggest_addresses(carparks_data_merged_df,address)
            if chosen_address:
                returned = search_carparks_data_from_address(carparks_data_merged_df, chosen_address)
                console.print(returned)

        elif choice == "exit":
            console.print("[bold green]Exiting program.[/bold green]")
            break
