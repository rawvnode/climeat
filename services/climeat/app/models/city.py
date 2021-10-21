from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
import datetime

from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models import city_response

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    year_reported = Column(Integer, nullable=False)
    account_number = Column(Integer, nullable=False)
    organization = Column(String(256), nullable=False)
    city = Column(String(512), nullable=False)
    country = Column(String(512), nullable=False)
    cdp_region = Column(String(512), nullable=False)
    reporting_authority = Column(String(512), nullable=True)
    access = Column(String(256), nullable=True)
    first_time_discloser = Column(String(256), nullable=True)
    population_year = Column(String(256), nullable=True)
    population = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
