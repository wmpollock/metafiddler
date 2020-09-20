#!/bin/env python3

"""Test for metafiddler.config"""
import logging
import pathlib
import unittest

from unittest.mock import patch, mock_open, Mock
import requests_mock

from metafiddler.config import MufiConfig


class TestConfig(unittest.TestCase):
    """Test configuration methods"""

    mock_config = {
        "current_page_get_url": "https://path/to/some/server",
        "metafiddler_root": "C:\\Users\\Bill\\Music\\MetaFilter",
        "playlists": {
            "playlist_a": {
                "list_id": 12345,
                "list_title": "Playlist A",
            },
            "playlist_b": {
                "list_id": 6789,
                "list_title": "Playlist B",
            },
            "playlist_x": {
                "list_id": 42424, 
                "list_title": "Playlist X"
            },
            "playlist_y": {
                "list_id": 14011, 
                "list_title": "Playlist Y"
            },
        },
    }

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            level=logging.CRITICAL, format="%(asctime)s [%(levelname)s] %(message)s"
        )

    @patch("yaml.load", return_value=mock_config)
    @patch("metafiddler.config.requests.get")
    def test_init(self, requests, yaml):
        """Test configuration load/setup"""
        # This test only works when the current_page_get_url is null :O
        # with self.assertRaises(SystemExit):
        #     print(vars(MufiConfig()))

        requests.return_value = Mock(status_code=200, response_text="YAYYY")
        config = MufiConfig()
        self.assertIsNotNone(config.current_page_url)

    def test_de64(self):
        self.assertIsNone(MufiConfig._de64("NONESUCH"))

    @requests_mock.Mocker()
    def test_update(self, request):
        """Test whether update works"""

        request.register_uri(requests_mock.ANY, requests_mock.ANY, text="7734")
        print("PAGE:", MufiConfig.current_page_post_url)
        config = MufiConfig()
        # https://github.com/otrabalhador/python-testing-by-examples/blob/master/docs/en/mocking/examples/reading-writing-on-files.md#writing-on-files
        with patch("builtins.open", mock_open()) as mocked_file:
            test_value = config.current_page_url
            print(f"Setting current page to {test_value}")

            config.current_page_url = test_value
            test_path = str(pathlib.Path.home() / ".metafiddler.current")
            mocked_file.assert_called_once_with(
                test_path, mode="w"
            )


if __name__ == "__main__":
    unittest.main()
