import json
import pandas as pd
from typing import List, Dict
from rich.console import Console
from utils.extract_rename_save_csv import extract_rename_save_csv
from utils.load_data_to_df import load_file_to_df
from utils.merge_data import merge_data
from utils.load_url_response import load_json_url_response
import numpy as np
console = Console()
# pd.options.mode.chained_assignment = None

def zomato_api_response_to_df(responses: List[Dict]) -> pd.DataFrame:
    """
    Converts a list of Zomato API responses into a pandas DataFrame.

    This function processes a list of API responses, extracts restaurant details,
    normalizes the JSON structure, and creates a pandas DataFrame.

    Args:
        responses (List[Dict]): A list of dictionaries, where each dictionary represents
            a Zomato API response containing restaurant data.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the extracted restaurant details.
    """
    all_restaurant_details = []

    for response in responses:
        interim_restaurant_details = response.get("restaurants", [])
        all_restaurant_details.extend([
            restaurant.get("restaurant")
            for restaurant in interim_restaurant_details
        ])

    restaurants_df = pd.json_normalize(all_restaurant_details)
    return restaurants_df

#call zomato api and retrieve restaurant details to restaurant_details.csv
def zomato_restaurant_countries_events_to_df(RESTAURANT_JSON_URL:str,DATA_FOLDER_DIR:str,COUNTRY_CODE_FILENAME:str,RESTAURANT_DETAILS_MAP:Dict):
    """
    Fetches restaurant data from a Zomato API URL, enriches it with country information,
    and expands the zomato_events column.

    Args:
        RESTAURANT_JSON_URL (str): The URL to fetch restaurant data from the Zomato API.
        DATA_FOLDER_DIR (str): The directory containing the 'Country-Codde' file.
        RESTAURANT_DETAILS_MAP(dict): Mapping of current df columns required to new names

    Returns:
        pandas.DataFrame: A DataFrame containing restaurant details enriched with country
                          information and expanded zomato_events.
    """
    #mock calling of zomato api into json_responses
    json_responses = load_json_url_response(RESTAURANT_JSON_URL)

    #parse responses to df
    restaurants_df = zomato_api_response_to_df(json_responses)

    #basic validation and data summary
    # print(restaurants_df.info())

    #fill empty fields with nan
    restaurants_df.fillna(np.nan,inplace=True)

    #load countries
    countries_df = load_file_to_df(f"{DATA_FOLDER_DIR}/{COUNTRY_CODE_FILENAME}")

    #merge countries_df and restaurants_df
    restaurants_countries_df,merge_logs = merge_data(restaurants_df,countries_df,"location.country_id","Country Code","inner")
    print(merge_logs)

    #expand zomate_events column
    restaurants_countries_expanded_df = restaurants_countries_df.explode('zomato_events')
    
    # print(filtered_restaurants_countries_expanded_df['zomato_events'][0])
    return restaurants_countries_expanded_df

def zomato_restaurant_details_to_csv(restaurant_details_df_main:pd.DataFrame,RESTAURANT_DETAILS_MAP:Dict,RESTAURANT_DETAILS_FILENAME:str,DATA_FOLDER_DIR:str):
    """
    Fetches dataframe that contains restaurant and country details with expanded events field

    Args:
        restaurant_details_df_main (pd.DataFrame)
        RESTAURANT_JSON_URL (str): The URL to fetch restaurant data from the Zomato API.
        DATA_FOLDER_DIR (str): The directory containing the 'Country-Code.xlsx' file.

    Returns:
        pandas.DataFrame: A DataFrame containing restaurant details with country
                          information and start date of each event according to map
    """
    #func to apply to restaurant_details_df to only leave event start date in event column
    def extract_and_convert_date(event_details):
        """
        Extracts the start date from event details.

        Args:
            event_details: A dictionary containing event information.

        Returns:
            pandas.Timestamp.date: A date object representing the start date if valid,
                                or 'NA' if the date is invalid or missing.
        """
        try:
            if isinstance(event_details, dict) and 'event' in event_details:
                date_str = event_details['event'].get('start_date')
                if date_str:
                    pd.to_datetime(date_str).date() #Check if it can be converted.
                    return pd.to_datetime(date_str).date()
            return np.nan
        except (ValueError, TypeError): 
            return np.nan
        except:
            return np.nan
    #create copy
    restaurant_details_df = restaurant_details_df_main.copy()
    try:
        #apply above function extract start date of event
        restaurant_details_df['zomato_events'] = restaurant_details_df['zomato_events'].apply(extract_and_convert_date)
        #convert user_aggregate_rating to float type
        restaurant_details_df["user_rating.aggregate_rating"] = restaurant_details_df["user_rating.aggregate_rating"].astype(float)
        #extract and save result
        extract_rename_save_csv(restaurant_details_df,DATA_FOLDER_DIR,RESTAURANT_DETAILS_FILENAME,RESTAURANT_DETAILS_MAP)
    except KeyError as e:
        print(f"KeyError: Missing key in DataFrame or mapping: {e}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: Could not save to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

