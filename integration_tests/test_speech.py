"""Test for metafiddler.speech"""
import unittest

from metafiddler.speech import Speaker
from metafiddler.config import MufiConfig

class TestConroller(unittest.TestCase):
    """test functions for metafiddler.speech"""
    def test_speech(self):
        """Test a basic utterance"""
        config = MufiConfig()
        s = Speaker(config)
        s.say("Audio test complete.")
