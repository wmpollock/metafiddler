"""Test for metafiddler.config"""
import pprint
import unittest
from metafiddler.config import MufiConfig


class TestConfig(unittest.TestCase):
    """Test configuration methods"""
    def test_config(self):
        """Test configuration load/setup"""
        config = MufiConfig()
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(vars(config))
        print(config.playlist_id("playlist_b"))
