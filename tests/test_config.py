"""Test for metafiddler.config"""
import logging
import pprint
import unittest
from unittest.mock import patch, mock_open
from metafiddler.config import MufiConfig


class TestConfig(unittest.TestCase):
    """Test configuration methods"""

    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )


    def test_config(self):
        """Test configuration load/setup"""
        config = MufiConfig()

        pretty = pprint.PrettyPrinter(indent=4)
        pretty.pprint(vars(config))
        print(config.playlist_id("playlist_b"))
        print("Current page:", config.current_page)
        print("Song save dir:", config.song_save_dir)

    def test_update(self):
        """Test whether update works"""
        config = MufiConfig()
        # https://github.com/otrabalhador/python-testing-by-examples/blob/master/docs/en/mocking/examples/reading-writing-on-files.md#writing-on-files
        with patch('builtins.open', mock_open()) as mocked_file:
            # This is a pretty janky case since we're just laying it down
            # but as its halfassedly mocked ATM its hitting live backend :O

            test_value = config.current_page
            print(f"Setting current page to {test_value}")
            config.current_page = test_value
            mocked_file.assert_called_once_with(config.state_file, mode='w')
            mocked_file().write.assert_called_once_with(test_value)
