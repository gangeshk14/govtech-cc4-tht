import pandas as pd
import warnings

def merge_data(df_left: pd.DataFrame, df_right: pd.DataFrame, left_key: str, right_key: str, merge_method: str) -> tuple[pd.DataFrame, dict]:
    """
    Merge two DataFrames on specified keys and method.
    
    Args:
        df1 (pd.DataFrame): First DataFrame.
        df2 (pd.DataFrame): Second DataFrame.
        left_key (str): Column name in df1 to merge on.
        right_key (str): Column name in df2 to merge on.
        merge_method (str): Merge method ('inner', 'left', 'right', 'outer').
    
    Returns:
        tuple: (Merged DataFrame, 
            logs dictionary with merge details
            logs_dict = {
                "total_rows_before",
                "total_rows_after",
                "unmatched_keys_in_df1",
                "unmatched_keys_in_df2"
                }
            )
    
    Raises:
        TypeError: If input is of the wrong type.
        ValueError: If the merge method is invalid.
        KeyError: If the specified keys do not exist in the DataFrames.
        RuntimeError: If merging fails due to any other reason.
    """
    try:
        #merge df
        merged_df = df_left.merge(df_right, left_on=left_key, right_on=right_key, how=merge_method)
        
        #count logs
        total_rows_before = len(df_left)
        total_rows_after = len(merged_df)
        unmatched_keys_left = set(df_left[left_key]) - set(df_right[right_key])
        unmatched_keys_right = set(df_right[right_key]) - set(df_left[left_key])
        
        logs_dict = {
            "total_rows_before": total_rows_before,
            "total_rows_after": total_rows_after,
            "unmatched_keys_in_df_left": unmatched_keys_left,
            "unmatched_keys_in_df_right": unmatched_keys_right
        }
        
        return merged_df, logs_dict
    except Exception as e:
        raise RuntimeError(f"Merging failed: {str(e)}")
