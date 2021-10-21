from datetime import datetime
from typing import Optional

from pydantic import BaseModel
    
class CityResponseBase(BaseModel):
    year_reported: Optional[int]
    account_number: Optional[int]
    organization: Optional[str]
    country: Optional[str]
    cdp_region: Optional[str]
    parent_section: Optional[str]
    section: Optional[str]
    question_number: Optional[str]
    question_name: Optional[str]
    column_number: Optional[int]
    column_name: Optional[str]
    row_number: Optional[int]
    row_name: Optional[str]
    response_answer: Optional[str]
    created_at: Optional[datetime]


class CityResponseCreate(CityResponseBase):
    ...

class CityResponseUpdate(CityResponseBase):
    id: Optional[int]

class CityResponseInDBBase(CityResponseBase):
    id: Optional[int]

    class Config:
        orm_mode = True

class CityResponse(CityResponseInDBBase):
    pass