"""Test for metafiddler.config"""
import pprint
import unittest
from metafiddler.config import MufiConfig
from unittest.mock import patch, mock_open
import logging

class TestConfig(unittest.TestCase):
    """Test configuration methods"""

    def setUp(self):
        logging.basicConfig(
           level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )
    

    def test_config(self):
        config = MufiConfig()
        """Test configuration load/setup"""
        
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(vars(config))
        print(config.playlist_id("playlist_b"))
        print("Current page:", config.current_page)            
        print("Song save dir:", config.song_save_dir)

    def test_update(self):
        """Test whether update works"""
        config = MufiConfig()
        # https://github.com/otrabalhador/python-testing-by-examples/blob/master/docs/en/mocking/examples/reading-writing-on-files.md#writing-on-files
        with patch('builtins.open', mock_open()) as mocked_file:
            test_value = 'foo'
            config.current_page = test_value
            mocked_file.assert_called_once_with(config.state_file, mode='w')
            mocked_file().write.assert_called_once_with(test_value)
