from typing import Text
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
import datetime

from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base

class CityResponse(Base):
    __tablename__ = "city_responses"
    id = Column(Integer, primary_key=True, index=True)
    year_reported = Column(Integer, nullable=False)
    account_number = Column(Integer)
    organization = Column(String(256), nullable=False)
    country = Column(String(512), nullable=False)
    cdp_region = Column(String(512), nullable=False)
    
    parent_section = Column(String(512), nullable=True)
    section = Column(String(256), nullable=True)
    question_number = Column(String(256), nullable=True)
    question_name = Column(Text, nullable=True)
    column_number = Column(Integer, nullable=True)
    column_name = Column(String(256), nullable=True)
    row_number = Column(Integer, nullable=True)
    row_name = Column(String(256), nullable=True)
    response_answer = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)