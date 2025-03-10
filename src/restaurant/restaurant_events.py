import pandas as pd
from typing import Dict
from utils.extract_rename_save_csv import extract_rename_save_csv

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
            start_date = pd.to_datetime(start_date_str).date() if start_date_str else 'NA'
            end_date = pd.to_datetime(end_date_str).date() if end_date_str else 'NA'
            title = event_details['event'].get('title', 'NA')
            event_id = event_details['event'].get('event_id', 'NA')
            return start_date, end_date, title, event_id
        return 'NA', 'NA', 'NA', 'NA'
    except (ValueError, TypeError):
        return 'NA', 'NA', 'NA', 'NA'
    
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
        return 'NA'
    except (ValueError, TypeError): 
        return 'NA'
    except:
        return 'NA'
#extract events
def extract_restaurant_events_by_mm_yyyy(mm_yyyy:str,expanded_zomato_restaurants_df:pd.DataFrame,DATA_FOLDER_DIR:str,RESTAURANTS_EVENT_MAP:Dict,RESTAURANT_EVENTS_FILENAME):

    # apply the function and store the results in two separate columns
    expanded_zomato_restaurants_df[['start_date', 'end_date','title','event_id']] = expanded_zomato_restaurants_df['zomato_events'].apply(lambda event: pd.Series(extract_dates_title_eventId(event)))
    # convert mm_yyyy to a datetime range and get start and end dates
    month, year = map(int, mm_yyyy.split('_'))
    start_of_month = pd.Timestamp(year, month, 1)
    end_of_month = start_of_month + pd.DateOffset(months=1) - pd.Timedelta(days=1)
    # filter rows where start_date or end_date falls within the specified month and year
    filtered_df = expanded_zomato_restaurants_df[
        ((expanded_zomato_restaurants_df['start_date'] != 'NA') & 
         (pd.to_datetime(expanded_zomato_restaurants_df['start_date'], errors='coerce').dt.date >= start_of_month.date()) & 
         (pd.to_datetime(expanded_zomato_restaurants_df['start_date'], errors='coerce').dt.date <= end_of_month.date())) |
        ((expanded_zomato_restaurants_df['end_date'] != 'NA') & 
         (pd.to_datetime(expanded_zomato_restaurants_df['end_date'], errors='coerce').dt.date >= start_of_month.date()) & 
         (pd.to_datetime(expanded_zomato_restaurants_df['end_date'], errors='coerce').dt.date <= end_of_month.date()))
    ]
    # extract photo details from filtered events
    filtered_df['photos'] = filtered_df['zomato_events'].apply(extract_photos)
    # expand the 'photos' column into separate rows
    filtered_photos_expanded_df = filtered_df.explode('photos')
    # extract the photo URL from each expanded row
    filtered_photos_expanded_df['photos'] = filtered_photos_expanded_df['photos'].apply(extract_photos_url)
    print(filtered_photos_expanded_df.head())

    #extract necessary columns and save
    extract_rename_save_csv(filtered_photos_expanded_df,DATA_FOLDER_DIR,RESTAURANT_EVENTS_FILENAME,RESTAURANTS_EVENT_MAP)
    return filtered_df
