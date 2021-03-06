import logging
from opentelemetry.trace import status
from starlette import responses
import uvicorn
import os

from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
# from fastapi.logger import logger as log

from typing import Optional, Any, List
from pathlib import Path
from sqlalchemy.orm import Session

from app.schemas.recipe import Recipe, RecipeSearchResults, RecipeCreate
from app import deps
from app import crud
from app.schemas.city import City
from app.crud import crud_city
from app.crud.crud_count import CountBase

from app.schemas.city_population import CityPopulation
from app.crud import crud_meat_city
from app.crud import crud_city_population
from app.schemas.meat_city import MeatPerCapita, MeatOverconsumption

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
AGENT_HOSTNAME = os.getenv("AGENT_HOST_NAME")


# logging.config.fileConfig('app/logging.conf', disable_existing_loggers=False)
# log = logging.getLogger("rich")

# from opentelemetry.exporter.richconsole import RichConsoleExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource



# EXPORTER: OTLPSpanExporter = OTLPSpanExporter(endpoint='otel-collector:4317')
EXPORTER: OTLPSpanExporter = OTLPSpanExporter(endpoint=f'{AGENT_HOSTNAME}:4317')
# EXPORTER: OTLPSpanExporter = OTLPSpanExporter(endpoint='192.168.1.77:4317')
TRACE_PROVIDER: TracerProvider = TracerProvider(
    resource = Resource.create(
        {
            "service.name" : 'og-muspell-recipe-app',
        }
    )
)

TRACE_PROVIDER.add_span_processor(BatchSpanProcessor(EXPORTER))
trace.set_tracer_provider(TRACE_PROVIDER)


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")
api_router = APIRouter()
log = logging.getLogger(__name__)

# Log formatter
class SpanFormatter(logging.Formatter):
    def format(self, record):
        trace_id = trace.get_current_span().get_span_context().trace_id
        if trace_id == 0:
            record.trace_id = None
        else:
            record.trace_id = "{trace:032x}".format(trace=trace_id)
        return super().format(record)

@app.on_event('startup')
def on_startup():
    print("adjusted trace order")
    FastAPIInstrumentor().instrument_app(app)    
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(SpanFormatter('time="%(asctime)s" service=%(name)s level=%(levelname)s %(message)s traceID=%(trace_id)s'))
    log.addHandler(handler)
    print("end of startup")

@app.on_event('shutdown')
def on_shutdown():
    FastAPIInstrumentor().uninstrument(app)

@api_router.get("/", status_code=200)
async def root(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    recipes = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": recipes},
    )

@api_router.get("/countcities/", status_code=200, response_model=CountBase)
async def get_count_cities(
    *
    , db: Session = Depends(deps.get_db)
) -> Any:
    print("og count cities")
    count = crud_city.get_count_cities(db)

    if not count:
        raise HTTPException(
            status_code=404, detail=f"Count not available."
        )

    return count

@api_router.get("/cities/", status_code=200, response_model=List[City])
async def get_cities(
    *
    , skip: int = 0
    , limit: int = 100
    , db: Session = Depends(deps.get_db)
) -> Any:
    print("og cities")
    cities = crud_city.get_cities(db, skip=skip, limit=limit)
    print(cities)

    if not cities:
        raise HTTPException(
            status_code=404, detail=f"City list not available."
        )    
    return cities

@api_router.get("/cities/{name}", status_code=200, response_model=City)
async def get_city(
    *
    , name: str
    , db: Session = Depends(deps.get_db)
) -> Any:
    print("Printing city")
    log.info("og city = {name}")

    result = crud_city.get_city(db, name)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"City {name} not found."
        )
    return result

@api_router.get("/populations/{name}", status_code=200, response_model=CityPopulation)
async def get_city_population(
    *
    , name: str
    , db: Session = Depends(deps.get_db)
) -> Any:
    log.info(f"og city = {name}")

    result = crud_city_population.get_population(db, name)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"City {name} not found."
        )
    return result

@api_router.get("/meatpercapita", status_code=200, response_model=List[MeatPerCapita])
async def get_meat_cities(
    *
    , db: Session = Depends(deps.get_db),
) -> Any:
    result = crud_meat_city.get_meat_cities(db)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Utopia"
        )
    return result

@api_router.get("/meatoverconsumption", status_code=200, response_model=List[MeatOverconsumption])
async def get_meat_cities(
    *
    , db: Session = Depends(deps.get_db),
) -> Any:
    result = crud_meat_city.get_meat_overconsumption(db)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Utopia"
        )
    return result


"""@api_router.get("/population", status_code=200, response_model=CityPopulation)
async def get_city_population(
    *
    , db: Session = Depends(deps.get_db)
) -> Any:
    print("og")
    result = crud_city_population.get_pops(db)
"""
@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single recipe by ID
    """
    log.info("og recipe id =")
    log.info("og recipe id =")

    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )
    log.info("og recipe id =")        
    return result

@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for recipes based on label keyword
    """
    log.info("og .......$$ search keyword=%s", keyword)    
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return { "results": recipes }

    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return { "results": list(results)[:max_results]}

@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(
    *,
    recipe_in: RecipeCreate,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new recipe in the database
    """
    log.info("og about to post")
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)
    return recipe

"""
@app.get("/")
async def root():
    return {"message": "Hello OG"}
"""

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

app.include_router(api_router)

import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    process_time = process_time * 1000 # convert to ms
    response.headers["X-Process-Time"] = str(process_time)
    log.info(f"ELAPSED={process_time} method={request.method} path={request.url.path} status_code={response.status_code}")
    return response


if __name__ == "__main__":
    log.info("og test")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True, log_level="debug")

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)