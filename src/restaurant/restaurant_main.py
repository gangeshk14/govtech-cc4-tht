import os
from dotenv import load_dotenv
from restaurant.restaurant_details import zomato_restaurant_countries_events_to_df,zomato_restaurant_details_to_csv
from restaurant.restaurant_events import extract_restaurant_events_by_mm_yyyy
from restaurant.restaurant_analysis import rating_text_thresholds_analyser
from utils.cli_funcs import prompt_user_yes_no
#constants
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
EVENT_MMYYY = "04_2019"

if __name__ == "__main__":
    #retrieving restaurants data and filtering columns
    restaurants_countries_expanded_df = zomato_restaurant_countries_events_to_df(RESTAURANT_JSON_URL,\
                                                                                 DATA_FOLDER_DIR,COUNTRY_CODE_FILENAME,RESTAURANT_DETAILS_MAP)
    #save restaurant_Details to csv
# Call the first function
if prompt_user_yes_no("Do you want to proceed with exporting restaurant details to CSV?"):
    zomato_restaurant_details_to_csv(restaurants_countries_expanded_df, RESTAURANT_DETAILS_MAP, RESTAURANT_DETAILS_FILENAME, DATA_FOLDER_DIR)

# Call the second function
if prompt_user_yes_no("Do you want to extract restaurant events by month and year?"):
    extract_restaurant_events_by_mm_yyyy(EVENT_MMYYY, restaurants_countries_expanded_df, DATA_FOLDER_DIR, RESTAURANTS_EVENT_MAP, RESTAURANT_EVENTS_FILENAME)

# Call the third function
if prompt_user_yes_no("Do you want to analyze rating text thresholds?"):
    rating_text_thresholds_analyser(restaurants_countries_expanded_df, RATING_TEXT_LIST, MIN_MAX_RATING)