import logging
import logging.config

import dotenv

from sqlalchemy_play.dbapi_transacations import DBAPITransactions
from sqlalchemy_play.db_metadata import DBMetaData

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)  # Add in SQLAlchemy with my overall logging
LOGGER = logging.getLogger(__name__)

dotenv.load_dotenv(override=True)  # load variables stored in .env, overwriting any system defined variables


def main():
    engine = DBAPITransactions.get_engine()
    DBAPITransactions(engine).run_all()
    DBMetaData(engine).run_all()


if __name__ == "__main__":
    LOGGER.info("Starting sqlalchemy_play")
    main()
