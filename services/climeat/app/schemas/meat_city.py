from datetime import datetime
from typing import Optional

from pydantic import BaseModel
    
class MeatBase(BaseModel):
    account: Optional[int]
    city: Optional[str]
    country: Optional[str]
    population: Optional[int]

class MeatPerCapita(MeatBase):
    meat_per_capita: Optional[float]

class MeatOverconsumption(MeatPerCapita):
    meat_overconsumption_kgs: Optional[float]
    meat_overconsumption_kpi: Optional[float]

