from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
import datetime

from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models import city_response

class CityPopulation(Base):
    __tablename__ = "city_populations"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, nullable=False)
    city = Column(String(512), nullable=False)
    population = Column(Integer, nullable=True)