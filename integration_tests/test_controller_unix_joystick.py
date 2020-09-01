""" Joystick integration tests for unix/pygame """

from metafiddler.input_events import InputEvent
from metafiddler.controller.unix.joystick import Joystick

from unittest import TestCase


class TestControllerUnixUSBJoystick(TestCase):
    """ Test yon Joystickerino """
    def test_joystick(self):
        """ Run the joystick setup """
        stick = Joystick()
        event = InputEvent.NONE
        while event == InputEvent.NONE:
            event = stick.poll()
        
        print("Got event", event.description)
        return True
