from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count

from app.crud.base import CRUDBase
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate
from app.crud.crud_count import CountBase

class CRUDCity(CRUDBase[City, CityCreate, CityUpdate]):
    def update(
        self, db: Session, *, db_obj: City, obj_in: Union[CityUpdate, Dict[str, Any]]
    ) -> City:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

city = CRUDCity(City)

def get_city(db: Session, name: str):
    return db.query(City).filter(City.city == name).filter(City.year_reported == 2020).first()

def get_cities(db: Session, skip: int = 0, limit: int = 100):
    print("og db get cities")
    return db.query(City).offset(skip).limit(limit).all()

def get_count_cities(db: Session):
    count = db.query(City).count()
    print(type(count))
    return CountBase(count=count)
