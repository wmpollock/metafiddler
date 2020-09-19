#!/bin/env python3

"""Test for metafiddler.config"""
import logging
import pprint
import unittest

from unittest.mock import patch, mock_open
import requests_mock

from metafiddler.config import MufiConfig

class TestConfig(unittest.TestCase):
    """Test configuration methods"""

    @classmethod
    def setUpClass(cls):
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

    @requests_mock.Mocker()
    def test_update(self, request):
        """Test whether update works"""

        request.register_uri(requests_mock.ANY, requests_mock.ANY, text='7734')
        print("PAGE:", MufiConfig.current_page_post_url)
        config = MufiConfig()
        # https://github.com/otrabalhador/python-testing-by-examples/blob/master/docs/en/mocking/examples/reading-writing-on-files.md#writing-on-files
        with patch('builtins.open', mock_open()) as mocked_file:
            test_value = config.current_page_url
            print(f"Setting current page to {test_value}")

            config.current_page_url = test_value
            mocked_file.assert_called_once_with('/home/bill/.metafiddler.current', mode='w')

if __name__ == "__main__":
    unittest.main()

