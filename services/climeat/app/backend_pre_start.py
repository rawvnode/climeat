import logging

from tenacity import after_log, before, before_log, retry, stop_after_attempt, wait_fixed

import sys
import os

from sqlalchemy.orm import session

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN)
)

def init() -> None:
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        logger.info("og database=%s", db)
    except Exception as e:
        logger.error(e)
        raise e

def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initialized")

if __name__ == "__main__":
    main()


