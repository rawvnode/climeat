from typing import List, Optional, Any
from pydantic import BaseModel, validator

class CountBase(BaseModel):
    count: int