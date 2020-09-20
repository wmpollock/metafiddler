""" Unix-specific gamepad/gamepad controller because a good cross-platform
controller with asynchronous polling seems nearly impossible to find """

import evdev

from metafiddler.controller.gamepadinterface import GamepadInterface
from metafiddler.input_events import InputEvent

BUTTON_CODE = 4
DIRECTION = 3

def device_is_gamepad(path):
    """ Filter a list of devices to find USB gamepads """
    device = evdev.InputDevice(path)
    # There's a trailing space for unknown reasons
    if device.name.startswith("USB Gamepad"):
        return True

    return False

class Gamepad(GamepadInterface):
    """ Unix Gamepad interface """
    gamepads = []

    def __init__(self):
        gamepad_devices = list(filter(device_is_gamepad, evdev.list_devices()))
        if not gamepad_devices:
            raise NotImplementedError()

        for gamepad_device in gamepad_devices:
            self.gamepads.append(evdev.InputDevice(gamepad_device))

    def poll(self):
        """ Get a gamepad event """

        retval = InputEvent.NONE
        for gamepad in self.gamepads:
            event = gamepad.read_one()

            # There are a sequence of events; we only care about the first it appears
            retval = self.translate_event(event)

            # Drain the rest of the events
            while event:
                event = gamepad.read_one()

        return retval

    def translate_event(self, event):
        button_map = {
            589825: "x",
            589826: "a",
            589827: "b",
            589828: "y",
            589829: "shoulder_l",
            589830: "shoulder_r",
            589833: "select",
            589834: "start",
        }
        directions = {
            # EVENT_CODE : EVENT.VAL
            0 : {
                0: "left",
                255: "right",
            },
            1 : {
                0: "up",
                255: "down",
            }

        }
        if event.val in button_map:
            button = button_map[event.val]
            return self.bindings[button]

        if event.type == DIRECTION and event.code in directions:
            return self.bindings[directions[event.code][event.val]]
        
        return InputEvent.NONE