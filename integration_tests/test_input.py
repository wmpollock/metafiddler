"""Providing for metafiddler.input"""

import unittest
from metafiddler.input import Input
from metafiddler.input_events import InputEvent


class TestConroller(unittest.TestCase):
    """Test controller functions"""

    def test_controls(self):
        """Test general control surface"""
        user_input = Input()
        print("Gimme anyol input:")
        event = InputEvent.NONE
        while event == InputEvent.NONE:
            event = user_input.poll()

        print("Got event", event.description)
        return True
