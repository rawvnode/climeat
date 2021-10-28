from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session, query_expression
from sqlalchemy.sql.functions import count

from app.crud.base import CRUDBase
from app.models.city_population import CityPopulation
from app.schemas.city_population import CityPopulationCreate, CityPopulationUpdate
from app.crud.crud_count import CountBase
from app.models import city_population
from app.schemas.city import City

from sqlalchemy import func, or_, and_, select, join

class CRUDCityPopulation(CRUDBase[CityPopulation, CityPopulationCreate, CityPopulationUpdate]):
    def update(
        self, db: Session, *, db_obj: CityPopulation, obj_in: Union[CityPopulationUpdate, Dict[str, Any]]
    ) -> CityPopulation:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

city_population = CRUDCityPopulation(CityPopulation)

def get_population(db: Session, name: str):
    return db.query(CityPopulation).filter(CityPopulation.city == name).first()

def get_pops(db: Session):
    results = db.query
    (
        select(
        [
            CityPopulation.population
        ]
        ).select_from(City)
        .where(City.year_reported == "2020")
    )
    print(results)
    return results