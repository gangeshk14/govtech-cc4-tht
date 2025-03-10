import requests
import json

def load_json_url_response(url:str):
    """
    Loads JSON data from a given URL.

    Args:
        url (str): The URL of the JSON file.

    Returns:
        dict or list or None: The parsed JSON data as a Python dictionary or list,
                             or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()  # Parse the JSON response
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}") #print the response to inspect it.
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None