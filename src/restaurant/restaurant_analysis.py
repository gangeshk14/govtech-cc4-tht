import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List
def rating_text_thresholds_analyser(restaurants_countries_expanded_df:pd.DataFrame,RATING_TEXT_LIST:List[str],MIN_MAX_RATING:tuple):
    """
    Analyzes restaurant rating data and computes dynamic rating thresholds for different rating texts.

    This function processes the restaurant review data by filtering relevant columns, cleaning missing values,
    visualizing the distribution of aggregate ratings, and plotting relationships between aggregate ratings, votes,
    and fake reviews. It also computes dynamic rating thresholds based on the minimum and maximum values of aggregate ratings
    for each rating text.

    Args:
        restaurants_countries_expanded_df (pd.DataFrame): A DataFrame containing the restaurant review data, with columns for
                                                        aggregate ratings, rating texts, votes, and fake reviews.
        RATING_TEXT_LIST (List[str]): A list of valid rating texts to filter the dataset (e.g., ['Poor', 'Average', 'Good', 'Very Good', 'Excellent']).
        MIN_MAX_RATING (tuple): A tuple containing the minimum and maximum rating values (e.g., (0, 5)) used to define rating ranges.

    Returns:
        dict: A dictionary containing the computed dynamic rating thresholds for each rating text. Each entry in the dictionary 
            maps a rating text to a tuple of (start_value, end_value), which defines the range for that rating text.
    """
    #step 1: filtering columns relevant to reviews
    restaurants_reviews_data_df = restaurants_countries_expanded_df[[
        'user_rating.aggregate_rating',
        'user_rating.rating_text',
        'user_rating.rating_color',
        'user_rating.votes',
        'user_rating.has_fake_reviews',
        'user_rating.custom_rating_text'
    ]].copy()
    # step 2: Drop rows where 'user_rating.aggregate_rating' or 'user_rating.rating_text' is None, NA, or NaN
    restaurants_reviews_data_df.dropna(subset=['user_rating.aggregate_rating', 'user_rating.rating_text'], inplace=True)

    #step 3: visualize data 
    for col in restaurants_reviews_data_df.columns:
        print(f"{col}: {restaurants_reviews_data_df[col].apply(type).value_counts().to_dict()}")
    print(restaurants_reviews_data_df['user_rating.rating_text'].unique())
    #step 3.1  only keep relevant text rating restaurants
    restaurants_reviews_data_df.drop(restaurants_reviews_data_df[~restaurants_reviews_data_df['user_rating.rating_text'].isin(RATING_TEXT_LIST)].index, inplace=True)

    #step 4 convert user_rating.aggregate_rating to float
    restaurants_reviews_data_df['user_rating.aggregate_rating'] = pd.to_numeric(restaurants_reviews_data_df['user_rating.aggregate_rating'], errors='coerce')
    restaurants_reviews_data_df.dropna(subset=['user_rating.aggregate_rating'], inplace=True)

    #step 5 convert user_rating.votes to int
    restaurants_reviews_data_df["user_rating.votes"] = pd.to_numeric(restaurants_reviews_data_df["user_rating.votes"], errors='coerce').fillna(0).astype(int)
    restaurants_reviews_data_df.drop(restaurants_reviews_data_df[restaurants_reviews_data_df["user_rating.votes"] == 0].index, inplace=True)

    #step 6
    # Plot Distribution of Aggregate Ratings
    plt.figure(figsize=(8,5))
    sns.histplot(restaurants_reviews_data_df['user_rating.aggregate_rating'], bins=20, kde=True, color="blue")
    plt.title("Distribution of Aggregate Ratings")
    plt.xlabel("Aggregate Rating")
    plt.ylabel("Frequency")
    plt.show()

    # Grouping by Rating Text and Analyzing Ratings
    rating_text_stats = restaurants_reviews_data_df.groupby('user_rating.rating_text')['user_rating.aggregate_rating'].agg(['min', 'max', 'mean', 'median', 'std', 'count'])


    # Visualizing relationships
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    sns.scatterplot(x=restaurants_reviews_data_df['user_rating.aggregate_rating'], y=restaurants_reviews_data_df['user_rating.votes'], alpha=0.6)
    plt.title("Aggregate Rating vs Votes")

    plt.subplot(1, 2, 2)
    sns.scatterplot(x=restaurants_reviews_data_df['user_rating.aggregate_rating'], y=restaurants_reviews_data_df['user_rating.has_fake_reviews'], alpha=0.6, color="red")
    plt.title("Aggregate Rating vs Fake Reviews")
    plt.show()
    
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='user_rating.rating_text', y='user_rating.aggregate_rating', data=restaurants_reviews_data_df, order=rating_text_stats.index)
    plt.xticks(rotation=45)
    plt.title("Aggregate Rating Distribution by Rating Text")
    plt.show()

    #assume not outliers given this is data from api response 
    category_rating_stats = rating_text_stats.sort_values(by="mean")
    print("\nAggregate Rating Ranges for Each Rating Text:")
    print(category_rating_stats)
    min_values = [float(val) for val in category_rating_stats['min'].values]
    max_values = [float(val) for val in category_rating_stats['max'].values]

    #to dynamcally extract threshold ranges
    min_values.append(MIN_MAX_RATING[1])
    rating_bins={}
    prev_end_val = None
    for idx, rating_text in enumerate(RATING_TEXT_LIST):
        if not prev_end_val:
            start_val = MIN_MAX_RATING[0]
        else:
            start_val = prev_end_val
        end_val = max(min_values[idx+1],max_values[idx])
        prev_end_val =end_val
        rating_bins[rating_text] = (start_val, end_val)
    print("\n Threshhold Ranges:")
    print(rating_bins)
    return rating_bins
