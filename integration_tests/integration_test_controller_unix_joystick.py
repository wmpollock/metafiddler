#!/usr/bin/env python3
 
""" Gamepad integration tests for unix/pygame """

from metafiddler.input_events import InputEvent
from metafiddler.controller.unix.gamepad import Gamepad

from unittest import TestCase


class TestControllerUnixUSBGamepad(TestCase):
    """ Test yon Gamepaderino """

    def test_gamepad(self):
        """ Run the gamepad setup """
        stick = Gamepad()
        event = InputEvent.NONE
        while event == InputEvent.NONE:
            event = stick.poll()

        print("Got event", event.description)
        return True

if __name__ == "__main__":
    unittest.main()
