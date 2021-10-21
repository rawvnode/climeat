from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.city_response import CityResponse
from app.schemas.city import CityCreate, CityUpdate
from app.schemas.city_response import CityResponseCreate, CityResponseUpdate

class CRUDCityResponse(CRUDBase[CityResponse, CityResponseCreate, CityResponseUpdate]):
    def update(
        self, db: Session, *, db_obj: CityResponse, obj_in: Union[CityResponseUpdate, Dict[str, Any]]
    ) -> CityResponse:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

city_response = CRUDCityResponse(CityResponse)