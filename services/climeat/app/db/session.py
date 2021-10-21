from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud.sqlcommenter.sqlalchemy.executor import BeforeExecuteFactory
import sqlalchemy
import logging

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://climeat:climeat@192.168.1.77:5432/climeat"

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