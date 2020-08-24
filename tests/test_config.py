"""Test for metafiddler.config"""
import logging
import os
import pprint
import requests
import requests_mock
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
        print("Current page:", config.current_page_url)
        print("Song save dir:", config.song_save_dir)
        self.assertIsNotNone(config.current_page_url)

    def test_update(self):
        """Test whether update works"""
        config = MufiConfig()
        config.current_page_post_url = "mock://foo.foo"
        # https://github.com/otrabalhador/python-testing-by-examples/blob/master/docs/en/mocking/examples/reading-writing-on-files.md#writing-on-files

        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock://', adapter)

        adapter.register_uri('GET', 'mock://foo.foo', text='data')
        with patch('builtins.open', mock_open()) as mocked_file:

            # Make sure we're testing safely...
            original_config_mtime = os.path.getmtime(config.config_file)

            test_value = config.current_page_url
            print(f"Setting current page to {test_value}")

            config.current_page_url = test_value
            mocked_file.assert_called_once_with(config.state_file, mode='w')
            self.assertTrue(mocked_file().write.assert_called_once_with(test_value))

            new_config_mtime = os.path.getmtime(config.config_file)
            self.assertEqual(original_config_mtime, new_config_mtime)
