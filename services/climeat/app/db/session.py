from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud.sqlcommenter.sqlalchemy.executor import BeforeExecuteFactory
import sqlalchemy
import logging
import os

POSTGRES_USER=os.getenv("POSTGRES_USER", "climeat")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "climeat")
POSTGRES_HOST=os.getenv("POSTGRES_HOST", "192.168.1.77")
POSTGRES_DB=os.getenv("POSTGRES_DB", "climeat")
POSTGRES_PORT=os.getenv("POSTGRES_PORT", "6000")

print("og print envs")
print(f"host = {POSTGRES_HOST}, port = {POSTGRES_PORT}, user = {POSTGRES_USER}")

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(SQLALCHEMY_DATABASE_URI)

log = logging.getLogger(__name__)

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    isolation_level="SERIALIZABLE"
)

listener = BeforeExecuteFactory(
    with_db_driver=True,
    with_db_framework=True,
    with_opentelemetry=True,
)
log.info("og before adding sql listener")
sqlalchemy.event.listen(engine, 'before_cursor_execute', listener, retval=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)