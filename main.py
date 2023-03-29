import logging
import logging.config

import dotenv

from sqlalchemy_play.play import Play

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)

dotenv.load_dotenv(override=True)  # load variables stored in .env, overwriting any system defined variables


def main():
    player = Play()
    player.log_stuff()
    player.say("Logging is configured. Yay!")


if __name__ == "__main__":
    LOGGER.info("Starting sqlalchemy_play")
    main()
