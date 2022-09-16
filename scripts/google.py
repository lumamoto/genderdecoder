from keys import GOOGLE_SEARCH_API_KEY
import genderdecoder.gd as gd
from serpapi import GoogleSearch
import pandas as pd

QUERIES = [
    "software engineer",
    "scientist",
    "data scientist",
    "engineer"
]

NUM_JOBS = 150


def main():
    # For each query...
    for query in QUERIES:
        print(f"========== Query: {query}")
        # Replace spaces with underscores for csv name
        csv_name = f"data/google/{query.replace(' ', '_')}.csv"
        # Get data and write to csv
        get_data(query, csv_name)
        # Get gender info and write to same csv
        determine_bias(csv_name)


def get_data(query, csv):
    '''
    Gets data by running API calls and writes it to a CSV.

    csv - The name of the .csv to save the data to.
    '''
    OFFSET = 10
    df = pd.DataFrame()

    start = 0
    while start < NUM_JOBS:
        print(f"Start: {start}")
        params = {
            "api_key": GOOGLE_SEARCH_API_KEY,
            "engine": "google_jobs",
            "google_domain": "google.com",
            "q": query,
            "hl": "en",  # English
            "gl": "us",  # Use United States for Google search
            "location": "United States",
            "start": start  # Offset
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        try:
            res_dict_list = results["jobs_results"]
            res_df = pd.DataFrame.from_records(res_dict_list)
            df = pd.concat([df, res_df])
        except:
            print("- An exception occurred!")
            break

        start += OFFSET

    df.to_csv(csv)


def determine_bias(csv):
    '''
    Uses assess() from genderdecoder package and adds results to DataFrame.
    Also adds columns for number of masculine and feminine coded words in 
    each job's lists.

    csv - The name of the .csv to read from and save the data to.
    '''
    df = pd.read_csv(csv)

    # Assess each row using genderdecoder
    df['res'] = df.apply(
        lambda row: gd.assess(row['description']), axis=1)
    # Turn res dict into Series
    df['res'].apply(pd.Series)
    # Drop res column and combine Series with rest of df
    df = pd.concat([df.drop(['res'], axis=1),
                    df['res'].apply(pd.Series)], axis=1)

    # Get length of masculine and feminine coded word lists
    if 'num_masculine_words' in df and 'num_feminine_words' in df:
        df['num_masculine_words'] = df.apply(
            lambda row: len(row['masculine_coded_words']), axis=1)
        df['num_feminine_words'] = df.apply(
            lambda row: len(row['feminine_coded_words']), axis=1)

    df.to_csv(csv)


if __name__ == "__main__":
    main()
