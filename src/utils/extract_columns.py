import pandas as pd
from typing import List
import warnings

def extract_columns(df: pd.DataFrame, extract_cols: List[str]) -> pd.DataFrame:
    """
    Extracts specified columns from a Pandas DataFrame.

    Args:
        df (pd.Dataframe): The input Pandas DataFrame.
        extract_cols (List[str]): A list of columns names to extract based as columns.

    Raises:
        KeyError: If any specified column name or index is not found in the DataFrame.

    Warnings:
        UserWarning: If one or more requested columns have duplicate names in the DataFrame.
    """
    #check if columns with the same name exist, then check if user has requested the return of any of those columns
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Error: The provided input is not a Pandas DataFrame.") from None
    if any(df.columns.duplicated()):
        duplicated_cols = set(df.columns[df.columns.duplicated(keep=False)].tolist())
        if any(col in duplicated_cols for col in extract_cols):
            warnings.warn("Warning: There is more than one column with the same name that you want to extract", UserWarning)
        
    #extract and return columns. raise error if column not found 
    try:
        return df[extract_cols]
    except KeyError as e:
        raise KeyError(f"Error: One or more column names/indices not found in the DataFrame: {e}")
