#!/bin/env python3

"""Test for metafiddler.input_events """
import logging
import unittest
from metafiddler.input_events import InputEvent, EventType


class TestInputEvents(unittest.TestCase):
    """Test input_events methods"""

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
        for event in events:
            self.assertIsNotNone(event.description)


if __name__ == "__main__":
    unittest.main()
