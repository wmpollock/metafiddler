""" Pysical test of controller interfaces,

Connect and go:  Ctrl-C ends the party
 """

import unittest

from metafiddler.input import Input
from metafiddler.input_events import InputEvent

class TestController(unittest.TestCase):
    """Test controller functions"""

    def test_controls(self):
        """Test general control surface"""
        user_input = Input()
        print("Gimme anyol input:")
        event = InputEvent.NONE
        while event == InputEvent.NONE:
            event = user_input.poll()

        print("Event:", event)
        print("Got event", event.description)
        self.assertIsNotNone(event)
