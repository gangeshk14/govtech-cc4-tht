import os
from dotenv import load_dotenv
from restaurant.restaurant_details import zomato_restaurant_countries_events_to_df,zomato_restaurant_details_to_csv
from restaurant.restaurant_events import extract_restaurant_events_by_mm_yyyy
#load env
load_dotenv()
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
DATA_FOLDER_DIR = os.getenv("DATA_FOLDER_DIR")
RESTAURANT_JSON_URL = os.getenv("RESTAURANT_JSON_URL")
RESTAURANT_DETAILS_FILENAME = os.getenv("RESTAURANT_DETAILS_FILENAME")
COUNTRY_CODE_FILENAME = os.getenv("COUNTRY_CODE_FILENAME")
RESTAURANT_EVENTS_FILENAME=os.getenv("RESTAURANT_EVENTS_FILENAME")
EVENT_MMYYY = "04_2019"
if __name__ == "__main__":
    #retrieving restaurants data and filtering columns
    restaurants_countries_expanded_df = zomato_restaurant_countries_events_to_df(RESTAURANT_JSON_URL,\
                                                                                 DATA_FOLDER_DIR,COUNTRY_CODE_FILENAME,RESTAURANT_DETAILS_MAP)
    #save restaurant_Details to csv
    # zomato_restaurant_details_to_csv(restaurants_countries_expanded_df,RESTAURANT_DETAILS_MAP,RESTAURANT_DETAILS_FILENAME,DATA_FOLDER_DIR)
    extract_restaurant_events_by_mm_yyyy(EVENT_MMYYY,restaurants_countries_expanded_df,DATA_FOLDER_DIR,RESTAURANTS_EVENT_MAP,RESTAURANT_EVENTS_FILENAME)