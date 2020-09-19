""" Unix-specific gamepad/gamepad controller because a good cross-platform
controller with asynchronous polling seems nearly impossible to find """

import evdev
from evdev import InputDevice, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like

from metafiddler.controller.gamepadinterface import GamepadInterface
from metafiddler.input_events import InputEvent

def deviceIsGamepad(path):
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
        gamepad_devices = list(filter(deviceIsGamepad, evdev.list_devices()))
        if not gamepad_devices:
            raise NotImplementedError()
        
        for gamepad_device in gamepad_devices:
            self.gamepads.append(evdev.InputDevice(gamepad_device))

        print("Init gamepad")
        self.gamepad = InputDevice("/dev/input/js0")
        
    def poll(self):
        """ Get a gamepad event """
        for gamepad in self.gamepads:
            event = gamepad.read_one()

            # Drain the rest of the events
            while event:
                event = gamepad.read_one()

