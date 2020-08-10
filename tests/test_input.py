"""Providing for metafiddler.input"""

import unittest
from metafiddler.input import Input
from metafiddler.events.input import Event


class TestConroller(unittest.TestCase):
    """Test controller functions"""

    def test_controls(self):
        """Test general control surface"""
        user_input = Input()
        e = user_input.poll()
        print("Gimme anyol input:")
        e = Event.NONE
        while e == Event.NONE:
            e = user_input.poll()

        print("Got event", Event.describe(e))
        return True
