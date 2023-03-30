import logging
import logging.config

import dotenv

from sqlalchemy_play.play import Play

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)  # Add in SQLAlchemy with my overall logging
LOGGER = logging.getLogger(__name__)

dotenv.load_dotenv(override=True)  # load variables stored in .env, overwriting any system defined variables


def main():
    play = Play()
    play.run_all()


if __name__ == "__main__":
    LOGGER.info("Starting sqlalchemy_play")
    main()
