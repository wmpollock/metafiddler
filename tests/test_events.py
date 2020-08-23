"""Test for metafiddler.events.inpyt """
import logging
import pprint
import unittest
from unittest.mock import patch, mock_open
from metafiddler.input_events import InputInputEvents, InputEventType

class TestConfig(unittest.TestCase):
    """Test configuration methods"""

    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )

    def test_init(self):
        event = InputEventType("stop", "in the name of love")
        self.assertNotEqual(event, None)
        self.assertNotEqual(InputEvents.NONE, EVENTS.PLAY)

    def test_list_events(self):
        