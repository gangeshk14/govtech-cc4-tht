import pandas as pd
from pandas import json_normalize
from typing import Optional, Union
import os
import json

def load_file_to_df(file_path: str, separator: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from various file types (CSV, Excel, etc.) into a DataFrame.
    The function automatically detects the file type based on the extension and uses the appropriate 
    pandas function to load the data into a DataFrame.

    Args:
        file_path (str): Path to the file.
        separator (str, optional): The separator for CSV or TSV files. If not provided, default (',' or '\t') is used.

    Returns:
        pd.DataFrame: Loaded data.

    Raises:
        RuntimeError: If an error occurs while loading the file or if the file type is unsupported.
        FileNotFoundError: If the file does not exist at the provided file path.
    """

    #get file extension
    file_extension = file_path.split('.')[-1].lower()

    # map file extension to respective pd loading func
    loaders = {
        'csv': lambda: pd.read_csv(file_path, sep=separator or ','),
        'xls': lambda: pd.read_excel(file_path),
        'xlsx': lambda: pd.read_excel(file_path),
        'parquet': lambda: pd.read_parquet(file_path),
        'tsv': lambda: pd.read_csv(file_path, sep=separator or '\t'),
    }
    try:
        return loaders[file_extension]() 
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except KeyError:
        raise ValueError(f"Unsupported file type: .{file_extension}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the file: {str(e)}") from e

def load_json_to_df(json_data: Union[str, dict, list]) -> pd.DataFrame:
    """
    Convert a JSON object (e.g., API response) into a pandas DataFrame.
    
    Args:
        json_data (Union[str, dict, list]): JSON data as a string, dictionary, or list.

    Returns:
        pd.DataFrame: DataFrame representation of the JSON data.

    Raises:
        ValueError: If the JSON data is invalid or cannot be converted to a DataFrame.
    """
    try:
        # If json_data is a string, attempt to parse it as JSON
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        # Normalize JSON structure to flatten nested lists/dictionaries
        df = json_normalize(json_data)
        return df
    except Exception as e:
        raise ValueError(f"Error processing JSON data: {e}") from e