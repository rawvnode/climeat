from datetime import datetime
from typing import Optional

from pydantic import BaseModel
    
class CityPopulationBase(BaseModel):
    account_number: Optional[int]
    city: Optional[str]
    population: Optional[int]

class CityPopulationCreate(CityPopulationBase):
    ...

class CityPopulationUpdate(CityPopulationBase):
    id: Optional[int]

class CityPopulationInDBBase(CityPopulationBase):
    id: Optional[int]

    class Config:
        orm_mode = True

class CityPopulation(CityPopulationInDBBase):
    pass