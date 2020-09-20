#!/bin/env python3

"""Test for metafiddler.config"""
import logging
import pprint
import unittest

from unittest.mock import patch, mock_open, Mock
import requests_mock

from metafiddler.config import MufiConfig


class TestConfig(unittest.TestCase):
    """Test configuration methods"""

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            level=logging.CRITICAL, format="%(asctime)s [%(levelname)s] %(message)s"
        )

    @patch("metafiddler.config.requests.get", )
    def test_config(self, requests):
        """Test configuration load/setup"""
        with self.assertRaises(SystemExit):
            MufiConfig()

        requests.return_value=Mock(status_code=200,response_text='YAYYY')
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
            mocked_file.assert_called_once_with(
                "/home/bill/.metafiddler.current", mode="w"
            )


if __name__ == "__main__":
    unittest.main()
