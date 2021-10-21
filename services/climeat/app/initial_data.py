import logging
import pandas as pd

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.db.base import Base
from app.db.init_db import init_db_cities, count_cities, count_city_responses, init_db_city_responses
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
    db = SessionLocal()
    count = count_cities(db)
    print(type(count))
    print(count)
    if count <= 0:
        cdp_df = load_data_csv_cities()
        print(cdp_df)
        print(type(cdp_df))
        init_db_cities(db, cdp_df)

    count = count_city_responses(db)
    print(type(count))
    print(count)
    if count <= 0:
        city_response_df = load_data_csv_city_responses()
        print(city_response_df.head())
        init_db_city_responses(db, city_response_df)

def load_data_csv_city_responses():
    dfs = {}
    for dirname, _, filenames in os.walk('datasets/'):
        for filename in filenames:
            df_path = os.path.join(dirname, filename)
            df_name = filename[:-4]
            if filename.split('.')[-1] == 'csv':
                dfs[df_name] = pd.read_csv(df_path)
            else:
                print("og ignoring non-csv file: ", filename)
    print('Loaded the following files: ', sorted(list(dfs.keys())))

    cr_2018_df = dfs['2018_Full_Cities_Dataset']
    cr_2019_df = dfs['2019_Full_Cities_Dataset']
    cr_2020_df = dfs['2020_Full_Cities_Dataset']

    cdp_df = cr_2018_df.append([cr_2019_df, cr_2020_df])

    cdp_df['Row Name'] = cdp_df['Row Name'].fillna('NA')
    cdp_df['Response Answer'] = cdp_df['Response Answer'].fillna('NA')
    cdp_df.drop('Questionnaire', axis=1, inplace=True)
    cdp_df.drop('Comments', axis=1, inplace=True)
    cdp_df.drop('File Name', axis=1, inplace=True)
    cdp_df.drop('Last update', axis=1, inplace=True)

    index = cdp_df.index
    num_rows = len(index)

    return cdp_df    

def load_data_csv_cities():
    dfs = {}
    for dirname, _, filenames in os.walk('datasets/'):
        for filename in filenames:
            df_path = os.path.join(dirname, filename)
            df_name = filename[:-4]
            if filename.split('.')[-1] == 'csv':
                dfs[df_name] = pd.read_csv(df_path)
            else:
                print("og ignoring non-csv file: ", filename)
    print('Loaded the following files: ', sorted(list(dfs.keys())))

    cd_2018_df = dfs['2018_Cities_Disclosing_to_CDP']
    cd_2019_df = dfs['2019_Cities_Disclosing_to_CDP']
    cd_2020_df = dfs['2020_Cities_Disclosing_to_CDP']

    cdp_df = cd_2018_df.append([cd_2019_df, cd_2020_df])
    cdp_df['Population'] = cdp_df['Population'].fillna(0)
    cdp_df['City'] = cdp_df['City'].fillna('NA')
    cdp_df['City Location'] = cdp_df['City Location'].fillna("POINT (0.0.0.0")

    index = cdp_df.index
    num_rows = len(index)

    return cdp_df    

def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")

if __name__ == "__main__":
    main()