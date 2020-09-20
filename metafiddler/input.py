"""Given a variety of potential input means, the Input class seeks to simplify them
into a singular access point and let this sort things out"""

import sys
from metafiddler.input_events import InputEvent

controllers = []  # pylint: disable=invalid-name

try:
    # This of course uses mscvrt which is not available on linux
    import metafiddler.controller.windows.keyboard
    import metafiddler.controller.windows.gamepad

    controllers.append(metafiddler.controller.windows.keyboard.Keyboard())
    controllers.append(metafiddler.controller.windows.gamepad.Gamepad())

except ModuleNotFoundError:
    print("Can't add Windows controllers.  Defaulting to unix...")
    try:
        import metafiddler.controller.unix.keyboard
        import metafiddler.controller.unix.gamepad

        controllers.append(metafiddler.controller.unix.keyboard.Keyboard())
        controllers.append(metafiddler.controller.unix.gamepad.Gamepad())

    except Exception as err:
        print(f"Can't add Unix system controllers: {err}")

try:


class Input:  # pylint: disable=too-few-public-methods
    """Class to streamline all input events from the user"""

    last_events = [InputEvent.NONE, InputEvent.NONE]

    def __init__(self):
        if not controllers:
            print("FATAL: no input controllers found.")
            sys.exit(1)

    def poll(self):
        """See if there is any input on this device"""
        for index, controller in enumerate(controllers):
            event = controller.poll()
            if self.last_events[index] != event:
                self.last_events[index] = event
                return event

        return InputEvent.NONE
