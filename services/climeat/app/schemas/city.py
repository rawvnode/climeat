from datetime import datetime
from typing import Optional

from pydantic import BaseModel
    
class CityBase(BaseModel):
    year_reported: Optional[int]
    account_number: Optional[int]
    organization: Optional[str]
    city: Optional[str]
    country: Optional[str]
    cdp_region: Optional[str]
    reporting_authority: Optional[str]
    access: Optional[str]
    first_time_discloser: Optional[str]
    population_year: Optional[str]
    population: Optional[int]
    created_at: Optional[datetime]
    # updated_at: Optional[datetime]

class CityCreate(CityBase):
    ...

class CityUpdate(CityBase):
    id: Optional[int]

class CityInDBBase(CityBase):
    id: Optional[int]

    class Config:
        orm_mode = True

class City(CityInDBBase):
    pass