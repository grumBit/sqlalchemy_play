import logging
import logging.config

import dotenv

from sqlalchemy_play.dbapi_transacations import DBAPITransactions
from sqlalchemy_play.db_metadata import DBMetaData
from sqlalchemy_play.data_interactions import DataInteractions

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)  # Add in SQLAlchemy with my overall logging
LOGGER = logging.getLogger(__name__)

dotenv.load_dotenv(override=True)  # load variables stored in .env, overwriting any system defined variables


def main():
    engine = DBAPITransactions.get_engine()
    DBAPITransactions(engine).run_all()
    DBMetaData(engine).run_all()
    DataInteractions(
        engine=engine,
        user_table=DBMetaData.get_user_account_table(),
        address_table=DBMetaData.get_address_table(),
    ).run_all()

    from sqlalchemy_play import play_orm
    from sqlalchemy_play.grum_delete_all_util import delete_all

    app_registry = play_orm.Base.registry
    # delete_all(app_registry, engine)


if __name__ == "__main__":
    LOGGER.info("Starting sqlalchemy_play")
    main()
