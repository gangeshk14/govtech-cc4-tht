import pandas as pd
from utils.extract_columns import extract_columns
from typing import Dict,Optional

def extract_rename_save_csv(df:pd.DataFrame,dir:str,file_name:str,column_map:Optional[Dict]):
    """
    Extracts specified columns from a DataFrame, renames them based on the provided mapping, 
    and saves the filtered and optionally renamed DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        dir (str): The directory where the CSV file will be saved.
        file_name (str): The name of the CSV file to save the DataFrame to.
        column_map (Optional[Dict]): A dictionary mapping the current column names to the new names.
                                        If no mapping is provided, columns are not renamed.

    Returns:
        None

    Side Effects:
        Saves the filtered DataFrame to a CSV file in the specified directory.
    """
    # extract the required columns based on the column_map keys
    filtered_df = extract_columns(df,column_map.keys())
   # check if column renaming is needed
    if not column_map.values():
        filtered_df.to_csv(f"{dir}/{file_name}", index=False) 
        print(f"Restaurant details saved to {file_name}")
    # rename and save 
    filtered_df = filtered_df.rename(columns=column_map)
    filtered_df.to_csv(f"{dir}/{file_name}", index=False) 
    print(f"Restaurant details saved to {file_name}")