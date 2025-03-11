import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import pytest
import pandas as pd
from extract_columns import extract_columns  # Replace 'your_module' with the actual module name

# Test data
@pytest.fixture
def sample_dataframe():
    """Fixture to create a sample DataFrame for testing."""
    return pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9],
        'D': [10, 11, 12]
    })

@pytest.fixture
def sample_dataframe_with_duplicates():
    """Fixture to create a DataFrame with duplicate column names."""
    df = pd.DataFrame([
    [1, 4, 7, 10],
    [2, 5, 8, 11],
    [3, 6, 9, 12]
    ])

    df.columns = ['A', 'B', 'C', 'A']
    return df

def test_extract_columns_valid(sample_dataframe):
    """
    Test valid extraction of columns.
    """
    result = extract_columns(sample_dataframe, ['A', 'B'])
    expected = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    pd.testing.assert_frame_equal(result, expected)

def test_extract_columns_duplicate_warning(sample_dataframe_with_duplicates):
    """
    Test that a warning is raised when extracting columns with duplicate names.
    """
    with pytest.warns(UserWarning, match="Warning: There is more than one column with the same name that you want to extract"):
        extract_columns(sample_dataframe_with_duplicates, ['A'])

def test_extract_columns_missing_column(sample_dataframe):
    """
    Test that a KeyError is raised when requesting a column that does not exist.
    """
    with pytest.raises(KeyError, match="Error: One or more column names/indices not found in the DataFrame"):
        extract_columns(sample_dataframe, ['X'])

def test_extract_columns_empty_dataframe():
    """
    Test that a KeyError is raised when extracting columns from an empty DataFrame.
    """
    df = pd.DataFrame()
    with pytest.raises(KeyError, match="Error: One or more column names/indices not found in the DataFrame"):
        extract_columns(df, ['A'])

def test_extract_columns_invalid_input():
    """
    Test that a TypeError is raised when the input is not a DataFrame.
    """
    with pytest.raises(TypeError):
        extract_columns("not_a_dataframe", ['A'])

def test_extract_columns_invalid_column_format(sample_dataframe):
    """
    Test that a KeyError is raised when column names are not strings or valid indices.
    """
    with pytest.raises(KeyError, match="Error: One or more column names/indices not found in the DataFrame"):
        extract_columns(sample_dataframe, [1.5])  # Invalid column format