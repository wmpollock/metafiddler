#!/bin/env python3

""" Unittest for Unix interfaces """

import unittest
from unittest.mock import Mock

from metafiddler.controller.unix.gamepad import Gamepad, GamepadInterface
from metafiddler.input_events import InputEvent

class EvEvent():
    """ Mock up the bogus event """
    def __init__(self, code, evtype, val):
        self.code = code
        self.type = evtype
        self.val = val
    def __str__(self):
        return f"Code: {self.code} Type: {self.type} Value: {self.val}"




def gamepads(code, evtype, val):
    fake_event = EvEvent(code,evtype,val)
    fake_gamepad =  Mock(**{"read_one.side_effect":[fake_event, None]})
    # fake_gamepad =  Mock(side_effect=[fake_event])

    return Mock(spec=Gamepad, **{
        "gamepads": [fake_gamepad]
    })




class TestGamepad(unittest.TestCase):
    """ Test the unix gamepad """
    reval=None

    def test_poll(self):
        self.assertEqual(
            InputEvent.NONE, 
            Gamepad.translate_event(GamepadInterface(), EvEvent(None, None, None))
        )
        # A
        self.assertEqual(
            InputEvent.PLAYLIST_A, 
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589826)))
        self.assertEqual(
            InputEvent.PLAYLIST_B,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589827))
        )

        self.assertEqual(
            InputEvent.PLAYLIST_X,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589825))
        )


        self.assertEqual(
            InputEvent.PLAYLIST_Y,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589828))
        )
        
        # Start button
        self.assertEqual(
            InputEvent.PLAY,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589834))
        )
        self.assertEqual(
            InputEvent.STOP,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589833))
        )
        self.assertEqual(
            InputEvent.SEEK_BACK,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589829))
        )
        self.assertEqual(
            InputEvent.SEEK_FORWARD,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589830))
        )
        self.assertEqual(
            InputEvent.VOLUME_DOWN,
            Gamepad.translate_event(GamepadInterface(), EvEvent(1, 3, 255))
        )
        self.assertEqual(
            InputEvent.VOLUME_UP,
            Gamepad.translate_event(GamepadInterface(), EvEvent(1, 3, 0))
        )
        self.assertEqual(
            InputEvent.PREVIOUS,
            Gamepad.translate_event(GamepadInterface(), EvEvent(0, 3, 0))
        )
        self.assertEqual(
            InputEvent.NEXT,
            Gamepad.translate_event(GamepadInterface(), EvEvent(0, 3, 255))
        )

        

if __name__ == "__main__":
    unittest.main()

