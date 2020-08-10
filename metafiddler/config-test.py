from metafiddler.config import MufiConfig
import unittest

class TestConfig(unittest.TestCase):
    def test_config(self):
        config = MufiConfig()
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(vars(config))
        print(config.playlist_id("playlist_b"))
