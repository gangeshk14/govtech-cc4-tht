# Project Name

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
  - [Restaurant Module](#restaurant-module)
    - [restaurant_main.py](#restaurant_main.py)
    - [restaurant_events.py](#restaurant_events.py)
    - [restaurant_details.py](#restaurant_details.py)
    - [restaurant_analysis.py](#restaurant_analysis.py)
  - [Carpark Module](#carpark-module)
  - [Utils Module](#utils-module)

## Introduction
Govtech THT Career 4.0

## Project Structure
```
project_root/
│── data/
│   └── Country-Code.xlsx
│── src/
│   ├── main.py
│   ├── restaurant/
│   │   ├── restaurant_main.py
│   │   ├── restaurant_events.py
│   │   ├── restaurant_details.py
│   │   └── restaurants_analysis.py
│   ├── carpark/
│   │   ├── carpark_main.py
│   │   ├── get_carparks_data.py
│   │   └── search_carparks_data.py
│   ├── utils/
│   │   ├── cli_funcs.py
│   │   ├── extract_columns.py
│   │   ├── extract_rename_save_csv.py
│   │   ├── load_data_to_df.py
│   │   ├── load_url_response.py
│   │   └── merge_data.py
|   |── tests/
└── README.md
```
##
[Video Demo Link]()
## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/gangeshk14/govtech-cc4-tht.git
   ```
2. Navigate to the project directory:
   ```sh
   cd govtech-cc4-tht
   ```
3. Create venv
  ```sh
  python -m venv .venv
  source .venv/bin/activate
  ```
4. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```
5. go to src directory
   ```sh
   cd src
  ```
6. run main module
  ```sh
  python -m main
  ```
7. run tests
  ```sh
  pytest
  ```
## Usage


## Modules
### Restaurant Module

`restaurant_main.py`: Entry point for restaurant-related operations.

`restaurant_events.py`: Gets events based on month and year.

`restaurant_details.py`: Extracts and processes restaurant details.

`restaurants_analysis.py`: 
#### Step 1: Retrieve columns relevant to reviews
- Select columns that contain review-related data (e.g., aggregate rating, votes, rating text, etc.)

#### Step 2: Drop rows where rating/rating_text is NA
- Remove rows where the aggregate rating or rating text is missing or null.

#### Step 3: Only keep rows with relevant text ratings
- Filter data to keep only rows with rating text values: `['Poor', 'Average', 'Good', 'Very Good', 'Excellent']`.

#### Step 4: Visualize column datatype(s)
- Check and visualize the data types of each relevant column in the dataset.

#### Step 5: Convert aggregate rating to float
- Convert the aggregate rating column to a float data type for numerical analysis.

#### Step 6: Convert votes to int
- Convert the votes column to an integer type to ensure proper numerical operations.

#### Step 7: Plot visualizations
- Distribution of Aggregate Ratings
- Visualizing relationships between:
  - Aggregate Rating vs Votes
  - Aggregate Rating vs Fake Reviews

#### Step 8: Box plot of Aggregate Rating Distribution by Rating Text
- Plot a box plot to show the distribution of aggregate ratings for each rating text (`['Poor', 'Average', 'Good', 'Very Good', 'Excellent']`).
- Calculate and display the following values:
  - Min
  - Max
  - Mean
  - Median
  - Standard Deviation (std)
  - Count

#### Step 9: Determine Rating Ranges for Prediction
- Focus on determining the min and max values for each `rating_text`.
- Based on the analysis, reviews are operating on a 0-5 scale.
- Loop through each `rating_text` to calculate its `start_rating_value` and `end_rating_value`:
  - The `start_rating_value` for each rating text will be the `end_rating_value` of the previous range (except for the first rating text where it will be 0).
  - The `end_rating_value` will be the maximum of the current range's maximum rating and the next range's minimum rating. 

### Carpark Module
Processes carpark-related data.
- `carpark_main.py`: Entry point for carpark-related operations.
- `get_carparks_data.py`: Fetches carpark data.
- `search_carparks_data.py`: Implements search functionality for carparks. Search by address and carpark num through cli. Search by address implements a version of autocomplete for cleaner ui

### Utils Module
Utility functions used across the project.
- `cli_funcs.py`: Command-line interface functions.
- `extract_columns.py`: Extracts specific columns from data and returns as df.
- `extract_rename_save_csv.py`: extracts required columns from df and saves as csv
- `load_data_to_df.py`: Loads data into pandas DataFrame.
- `load_url_response.py`: Fetches data from URLs.
- `merge_data.py`: Merges different dataframes.

## Data
Contains reference data used in the project.
- `Country-Code.xlsx`: Excel file with country codes.

## Testing

Basic testing for some functions are available.

