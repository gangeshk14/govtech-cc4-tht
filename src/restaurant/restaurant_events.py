import pandas as pd
from typing import Dict
from utils.extract_rename_save_csv import extract_rename_save_csv
import numpy as np
 #func to extract start and end dates of events in df
def extract_dates_title_eventId(event_details:Dict):
    """
    Extracts the start and end dates, title, and event ID from event details.

    Args:
        event_details (dict): A dictionary containing event information.

    Returns:
        tuple: A tuple containing (start_date, end_date, title, event_id). 
               If dates are missing or invalid, returns 'NA' instead.
    """
    try:
        if isinstance(event_details, dict) and 'event' in event_details:
            start_date_str = event_details['event'].get('start_date')
            end_date_str = event_details['event'].get('end_date')
            start_date = pd.to_datetime(start_date_str).date() if start_date_str else np.nan
            end_date = pd.to_datetime(end_date_str).date() if end_date_str else np.nan
            title = event_details['event'].get('title', np.nan)
            event_id = event_details['event'].get('event_id', np.nan)
            title_str = str(title) if not isinstance(title, float) or not np.isnan(title) else title
            event_id_str = str(event_id) if not isinstance(event_id, float) or not np.isnan(event_id) else event_id
            return start_date, end_date, title_str, event_id_str
        return np.nan, np.nan, np.nan , np.nan
    except (ValueError, TypeError):
        return np.nan, np.nan, np.nan , np.nan
    
#func to extract photos from events
def extract_photos(event_details):
    """
    Extracts photos from event details.

    Args:
        event_details: A dictionary containing event information.

    Returns:
        list: A list of photo URLs if available, else an empty list.
    """
    if isinstance(event_details, dict) and 'event' in event_details:
        return event_details['event'].get('photos', [])  # Default to empty list if 'photos' is missing
    return []
#func to apply to restaurant_details_df to only leave photos url
def extract_photos_url(photo_details:Dict):
    """
    Extracts the photo URL from photo details.

    Args:
        photo_details (dict): A dictionary containing photo details.

    Returns:
        str: The extracted photo URL if available; otherwise, returns 'NA'.
    """
    try:
        if isinstance(photo_details, dict) and 'photo' in photo_details:
            url_str = photo_details['photo'].get('url')
            if url_str:
                return url_str
        return np.nan
    except (ValueError, TypeError): 
        return np.nan
    except:
        return np.nan
#extract events
def extract_restaurant_events_by_mm_yyyy(mm_yyyy: str, expanded_zomato_restaurants_main_df: pd.DataFrame, DATA_FOLDER_DIR: str, RESTAURANTS_EVENT_MAP: Dict, RESTAURANT_EVENTS_FILENAME: str) -> pd.DataFrame:
    """
    Extracts and filters restaurant events based on a given month and year.

    Args:
        mm_yyyy (str): The month and year in 'MM_YYYY' format.
        expanded_zomato_restaurants_main_df (pd.DataFrame): DataFrame containing restaurant event details.
        DATA_FOLDER_DIR (str): Directory path to save the processed CSV file.
        RESTAURANTS_EVENT_MAP (dict): Mapping for renaming event-related columns.
        RESTAURANT_EVENTS_FILENAME (str): Filename for saving the processed event data.

    Returns:
        pd.DataFrame: The filtered DataFrame containing relevant events within the specified month and year.
    """
    try:
        #copy main df to avoid conflicts
        expanded_zomato_restaurants_df = expanded_zomato_restaurants_main_df.copy()
        #extract necessary event details to separate cols
        expanded_zomato_restaurants_df[['start_date', 'end_date', 'title', 'event_id']] = expanded_zomato_restaurants_df['zomato_events'].apply(lambda event: pd.Series(extract_dates_title_eventId(event)))

        #get date range to search from mm_yyyy string
        month, year = map(int, mm_yyyy.split('_'))
        start_of_month = pd.Timestamp(year, month, 1)
        end_of_month = start_of_month + pd.DateOffset(months=1) - pd.Timedelta(days=1)

        #convert start and end date columns to datetime
        expanded_zomato_restaurants_df['start_date'] = pd.to_datetime(expanded_zomato_restaurants_df['start_date'], errors='coerce')
        expanded_zomato_restaurants_df['end_date'] = pd.to_datetime(expanded_zomato_restaurants_df['end_date'], errors='coerce')

        #compare mm_yyyy range with every col's start and end date
        filtered_df = expanded_zomato_restaurants_df[
            ((expanded_zomato_restaurants_df['start_date'].notna()) &
             (expanded_zomato_restaurants_df['start_date'] >= start_of_month) &
             (expanded_zomato_restaurants_df['start_date'] <= end_of_month)) |
            ((expanded_zomato_restaurants_df['end_date'].notna()) &
             (expanded_zomato_restaurants_df['end_date'] >= start_of_month) &
             (expanded_zomato_restaurants_df['end_date'] <= end_of_month))
        ].copy()

        #extract photos, and then each photo's url link
        filtered_df['photos'] = filtered_df['zomato_events'].apply(extract_photos)
        filtered_photos_expanded_df = filtered_df.explode('photos')
        filtered_photos_expanded_df['photos'] = filtered_photos_expanded_df['photos'].apply(extract_photos_url)

        extract_rename_save_csv(filtered_photos_expanded_df, DATA_FOLDER_DIR, RESTAURANT_EVENTS_FILENAME, RESTAURANTS_EVENT_MAP)
        return filtered_df

    except Exception as e:
        print(f"Error in extract_restaurant_events_by_mm_yyyy: {e}")
        return pd.DataFrame()
