"""
Test for metafiddler.mechanize

Mocking pain points:

"""
import logging
import unittest

from unittest.mock import MagicMock

from metafiddler.config import MufiConfig
from metafiddler.mechanize import Browser


HOT_TEST = False

class TestMechanise(unittest.TestCase):
    """Test configuration methods"""

    def setUp(self):
        """ Work out the login routine """
        self.config = MufiConfig()
        self.browser = Browser(self.config)

        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )

    def test_login(self):
        """ Check the login process, or the mockery of the login process, as you like it"""
        if not HOT_TEST:
            print("SUBSTITUTING BROWSER")
            self.browser.browser = MagicMock(name='Browser()')

    def test_playlist_add(self):
        """Invoke adding a record to the playlist"""
        playlist = self.config.playlist_id("playlist_x")
        # pprint.pprint(self.config.playlists)
        print("Playlist:", playlist)

        self.browser.playlist_add(playlist, 8)
