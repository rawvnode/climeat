import logging
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app import crud, schemas
from app.models.city import City
from app.models.city_response import CityResponse
from app.db import base
from pandas import DataFrame

logger = logging.getLogger(__name__)

# ensure all SQL Alchemy models are imported (app.db.base) before init'ing DB
# otherwise SQL Alchemy might fail to init relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

def count_cities(db: Session) -> int:
    print("Count cities")
    count = db.query(City).count()
    print("og count = %s", count)
    return count

def count_city_responses(db: Session) -> int:
    print("Count city responses")
    count = db.query(CityResponse).count()
    print("og count = %s", count)
    return count

def init_db_cities(db: Session, cdp_df: DataFrame) -> None:
    print("og init_db...")
    print(cdp_df.head())
    for i, row in cdp_df.iterrows():
        print(row['Year Reported to CDP'])
        print(type(row['Year Reported to CDP']))
        city_in = schemas.CityCreate(
                year_reported=row['Year Reported to CDP']
                , account_number=row['Account Number']
                , organization=row['Organization']
                , city=row['City']
                , country=row['Country']
                , cdp_region=row['CDP Region']
                , reporting_authority=row['Reporting Authority']
                , access=row['Access']
                , first_time_discloser=row['First Time Discloser']
                , population_year=row['Population Year']
                , population=row['Population']
        )
        city = crud.city.create(db, obj_in=city_in)

def init_db_city_responses(db: Session, cdp_df: DataFrame) -> None:
    print("og init_db city_responses...")
    print(cdp_df.head())
    for i, row in cdp_df.iterrows():
        print(row['Year Reported to CDP'])
        print(type(row['Year Reported to CDP']))
        city_response_in = schemas.CityResponseCreate(
                year_reported=row['Year Reported to CDP']
                , account_number=row['Account Number']
                , organization=row['Organization']
                , country=row['Country']
                , cdp_region=row['CDP Region']
                , section=row['Section']
                , parent_section=row['Parent Section']
                , question_number=row['Question Number']
                , question_name=row['Question Name']
                , column_number=row['Column Number']
                , column_name=row['Column Name']
                , row_number=row['Row Number']
                , row_name=row['Row Name']
                , response_answer=row['Response Answer']
        )
        city_response = crud.city_response.create(db, obj_in=city_response_in)
