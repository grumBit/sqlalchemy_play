import logging
import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)

import dotenv
dotenv.load_dotenv(override=True) # load variables stored in .env, overwrting any system defined variables

from sqlalchemy_play.play import Play

def main():
    player = Play()
    player.log_stuff()
    player.say("Logging is configured. Yay!")



if __name__ == "__main__":
    LOGGER.info("Starting sqlalchemy_play")
    main()
