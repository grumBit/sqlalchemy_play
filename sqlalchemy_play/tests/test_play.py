import logging

import unittest

from mock import call, DEFAULT, MagicMock, patch
from os.path import dirname, basename

import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)

from sqlalchemy_play.play import Play


class PlayTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_say(self):
        self.assertIsNone(Play().say("something"))

