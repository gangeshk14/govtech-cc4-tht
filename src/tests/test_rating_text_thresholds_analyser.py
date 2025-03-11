import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../restaurant')))
import pytest
import pandas as pd
from typing import List
import matplotlib as plt
from restaurant_analysis import rating_text_thresholds_analyser 

@pytest.fixture
def sample_data():
    # Create a sample DataFrame for testing
    data = {
        'user_rating.aggregate_rating': [1.0, 2.5, 3.0, 4.5, 5.0, 2.0, 3.5, 4.0, 1.5, 2.8],
        'user_rating.rating_text': ['Poor', 'Average', 'Good', 'Very Good', 'Excellent', 'Poor', 'Good', 'Very Good', 'Poor', 'Average'],
        'user_rating.rating_color': ['red', 'yellow', 'green', 'blue', 'darkgreen'] * 2,
        'user_rating.votes': [10, 20, 30, 40, 50, 15, 25, 35, 5, 18],
        'user_rating.has_fake_reviews': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        'user_rating.custom_rating_text': [None] * 10
    }
    return pd.DataFrame(data)

def test_rating_text_thresholds_analyser(sample_data):
    # Define the rating text list and min-max rating tuple
    RATING_TEXT_LIST = ['Poor', 'Average', 'Good', 'Very Good', 'Excellent']
    MIN_MAX_RATING = (0, 5)

    # Call the function
    result = rating_text_thresholds_analyser(sample_data, RATING_TEXT_LIST, MIN_MAX_RATING)

    # Assert that the result is a dictionary
    assert isinstance(result, dict)

    # Assert that the dictionary contains the correct keys
    assert set(result.keys()) == set(RATING_TEXT_LIST)

    # Assert that the values are tuples with two elements
    for key, value in result.items():
        assert isinstance(value, tuple)
        assert len(value) == 2


# Run the test
if __name__ == "__main__":
    pytest.main()
