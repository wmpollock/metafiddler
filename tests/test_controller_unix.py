#!/bin/env python3

""" Unittest for Unix interfaces """

import unittest
from unittest.mock import Mock, patch

import metafiddler.controller.unix.gamepad
from metafiddler.controller.unix.gamepad import Gamepad, GamepadInterface
from metafiddler.input_events import InputEvent


class EvEvent:
    """ Mock up the bogus event """

    def __init__(self, code, evtype, val):
        self.code = code
        self.type = evtype
        self.val = val

    def __str__(self):
        return f"Code: {self.code} Type: {self.type} Value: {self.val}"


def mock_gamepad(code, evtype, val):
    """ Mock gamepad instance """
    fake_event = EvEvent(code, evtype, val)
    fake_gamepad = Mock(**{"read_one.side_effect": [fake_event, None]})
    # fake_gamepad =  Mock(side_effect=[fake_event])

    return Mock(spec=Gamepad, **{"gamepads": [fake_gamepad]})


class TestGamepad(unittest.TestCase):
    """ Test the unix gamepad """

    @patch("evdev.InputDevice")
    def test_device_is_gamepad(self, evdev):
        """ Test the __init__() function """
        evdev.return_value.name = "FOO"
        self.assertFalse(metafiddler.controller.unix.gamepad.device_is_gamepad("/foo"))

        evdev.return_value.name = "USB Gamepad "  # extra space like we get...
        self.assertTrue(metafiddler.controller.unix.gamepad.device_is_gamepad("/good"))

    @patch("evdev.InputDevice")
    @patch("evdev.list_devices", return_value=[])
    def test_init(self, evdev, inputdevice):
        """ Test the __init__() function """
        with self.assertRaises(NotImplementedError):
            Gamepad()
        evdev.return_value = [Mock()]
        self.assertIsInstance(Gamepad(), Gamepad)

    def test_poll(self):
        Gamepad.poll(mock_gamepad(4, 4, 589826))
        # self.assertEqual(
        #     InputEvent.PLAYLIST_A, )
        # )

    def test_translate_event(self):
        """ Test the buttonmappings """
        self.assertEqual(
            InputEvent.NONE,
            Gamepad.translate_event(GamepadInterface(), EvEvent(None, None, None)),
        )
        # A
        self.assertEqual(
            InputEvent.PLAYLIST_A,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589826)),
        )
        self.assertEqual(
            InputEvent.PLAYLIST_B,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589827)),
        )

        self.assertEqual(
            InputEvent.PLAYLIST_X,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589825)),
        )

        self.assertEqual(
            InputEvent.PLAYLIST_Y,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589828)),
        )

        # Start button
        self.assertEqual(
            InputEvent.PLAY,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589834)),
        )
        self.assertEqual(
            InputEvent.STOP,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589833)),
        )
        self.assertEqual(
            InputEvent.SEEK_BACK,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589829)),
        )
        self.assertEqual(
            InputEvent.SEEK_FORWARD,
            Gamepad.translate_event(GamepadInterface(), EvEvent(4, 4, 589830)),
        )
        self.assertEqual(
            InputEvent.VOLUME_DOWN,
            Gamepad.translate_event(GamepadInterface(), EvEvent(1, 3, 255)),
        )
        self.assertEqual(
            InputEvent.VOLUME_UP,
            Gamepad.translate_event(GamepadInterface(), EvEvent(1, 3, 0)),
        )
        self.assertEqual(
            InputEvent.PREVIOUS,
            Gamepad.translate_event(GamepadInterface(), EvEvent(0, 3, 0)),
        )
        self.assertEqual(
            InputEvent.NEXT,
            Gamepad.translate_event(GamepadInterface(), EvEvent(0, 3, 255)),
        )


if __name__ == "__main__":
    unittest.main()
