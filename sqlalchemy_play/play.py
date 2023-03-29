import logging

LOGGER = logging.getLogger(__name__)


class Play():

    def say(self, msg: str):
        LOGGER.info(f"Saying: {msg}")
        print(msg)

    def log_stuff(self):
        LOGGER.debug("debug message")
        LOGGER.info("info message")
        LOGGER.warning("warn message")
        LOGGER.error("error message")
        LOGGER.critical("critical message")

if __name__ == "__main__":
    player = Play()
    player.log_stuff()
    player.say("Logging isn't configured, so just default logging, which doesn't include debug, or files.")
