from utils.load_url_response import load_json_url_response
from utils.load_data_to_df import load_json_to_df, load_file_to_df
from utils.merge_data import merge_data
import pandas as pd
import numpy as np
from rich.console import Console
from typing import Dict
console = Console()

import numpy as np
 #func to extract start and end dates of events in df
def extract_carpark_info(carpark_info:Dict):
    """
    Extracts the start and end dates, title, and event ID from event details.

    Args:
        event_details (dict): A dictionary containing event information.

    Returns:
        tuple: A tuple containing (start_date, end_date, title, event_id). 
               If dates are missing or invalid, returns 'NA' instead.
    """
    try:
        if isinstance(carpark_info, dict):
            total_lots = carpark_info.get('total_lots')
            lot_type = carpark_info.get('lot_type')
            lots_available = carpark_info.get('lots_available')
            return total_lots, lot_type, lots_available
        return np.nan, np.nan, np.nan
    except (ValueError, TypeError):
        return np.nan, np.nan, np.nan
def get_carparks_data(CARPARKS_API_URL: str, CARPARK_STATIC_CSV_URL: str) -> pd.DataFrame:
    """
    Fetches and processes carpark availability data from an API and merges it with static carpark information from a CSV.

    Args:
        CARPARKS_API_URL (str): The URL of the API endpoint providing real-time carpark availability data in JSON format.
        CARPARK_STATIC_CSV_URL (str): The URL or file path of the CSV file containing static carpark information.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the merged carpark data, with real-time availability and static information.
                     Returns the merged dataframe after cleaning and validation.

    Raises:
        Exception: If there are issues loading data from the API or CSV, or during the merging process.
    """
    try:
        # Get API response
        response = load_json_url_response(CARPARKS_API_URL)

        # Extract carpark data
        items = response.get('items')
        carpark_data = items[0].get('carpark_data')
        carpark_data_df = load_json_to_df(carpark_data)
        carpark_data_df = carpark_data_df.explode('carpark_info')
        carpark_data_df[['total_lots', 'lot_type', 'lots_available']] = carpark_data_df['carpark_info'].apply(lambda carpark_info: pd.Series(extract_carpark_info(carpark_info)))

        # Load static carparks data from CSV
        static_carparks_df = load_file_to_df(CARPARK_STATIC_CSV_URL)

        # Merge dataframes on carpark number
        carpark_data_merged_df, merged_logs = merge_data(carpark_data_df, static_carparks_df, 'carpark_number',
                                                         'car_park_no', 'inner')

        # Validate data
        # Fill empty values with NaN
        carpark_data_merged_df.fillna(np.nan, inplace=True)

        # Check missing values
        missing_values = carpark_data_merged_df.isnull().sum()

        # Remove trailing spaces from object columns
        for col in carpark_data_merged_df.select_dtypes(include=['object']).columns:
            carpark_data_merged_df[col] = carpark_data_merged_df[col].str.strip()

        # Print data summary (optional)
        # print("Missing Values and Data Types per Column:")
        # for col in carpark_data_merged_df.columns:
        #     type_counts = carpark_data_merged_df[col].apply(type).value_counts().to_dict()
        #     console.print(f"{col}: Missing={missing_values[col]}, Types={type_counts}")
        return carpark_data_merged_df

    except Exception as e:
        raise RuntimeError(f"Failed to process carpark data: {e}")