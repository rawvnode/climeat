from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate

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