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

    def test_config(self, browser):
        """Test configuration load/setup"""
        config = MufiConfig()

        pretty = pprint.PrettyPrinter(indent=4)
        pretty.pprint(vars(config))
        print(config.playlist_id("playlist_b"))
        print("Current page:", config.current_page_url)
        print("Song save dir:", config.song_save_dir)
        self.assertIsNotNone(config.current_page_url)

