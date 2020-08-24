"""Test for metafiddler.input_events """
import logging
import unittest
from metafiddler.input_events import InputEvent, EventType

class TestConfig(unittest.TestCase):
    """Test configuration methods"""

    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )

    def test_init(self):
        """ Make sure the init works as advertised """
        event = EventType("stop", "in the name of love")
        self.assertNotEqual(event, None)
        self.assertNotEqual(InputEvent.NONE, InputEvent.PLAY)

    def test_list_events(self):
        """ Test events method """
        events = InputEvent.events()
        self.assertNotEqual(events, None)

        print(events)
        for event in events:
            print(event.description)
