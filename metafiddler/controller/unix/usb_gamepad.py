""" Unix-specific gamepad/gamepad controller because a good cross-platform
controller with asynchronous polling seems nearly impossible to find """

import evdev
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like

from metafiddler.controller.interface import ControllerInterface
from metafiddler.input_events import InputEvent

def deviceIsGamepad(path):
    """ Filter a list of devices to find USB gamepads"
    device = evdev.InputDevice(path)
    # There's a trailing space for unknown reasons
    if device.name.startswith("USB Gamepad"):
        return True

    return False

class Gamepad(ControllerInterface):
    """ Unix Gamepad interface"""

    def __init__(self):
        print(evdev.list_devices())
        print("Init gamepad")
        self.gamepad = InputDevice("/dev/input/js0")
        
    def poll(self):
        """ Get a gamepad event """
        event = self.gamepad.read_one()
        if event:
            print(event)

