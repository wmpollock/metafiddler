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
        e = InputEvent.NONE
        while e == InputEvent.NONE:
            e = user_input.poll()

        print("Got event", InputEvent.describe(e))
        return True
