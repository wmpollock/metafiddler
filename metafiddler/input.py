"""Given a variety of potential input means, the Input class seeks to simplify them
into a singular access point and let this sort things out"""

from metafiddler.events.input import Event

controllers = []

try:
    import metafiddler.controller.windows.keyboard
    controllers.append(metafiddler.controller.windows.keybord.Keyboard())
except:
    print("Can't add Windows USB Keyboard")

    import metafiddler.controller.keyboard
    controllers.append(metafiddler.controller.keyboard.Keyboard())

try:
    import metafiddler.controller.windows.usb_joystick
    controllers.append(metafiddler.controller.windows.usb_joystick.Joystick())
except Exception as e:
    print("Can't add Windows USB Joystick")



class Input:
    """Class to streamline all input events from the user"""
    last_events = [Event.NONE, Event.NONE]

    def __init__(self):
        if len(controllers) == 0:
            print("FATAL: no input controllers found.")
            exit(1)

    def poll(self):
        """See if there is any input on this device"""
        for x in range(len(controllers)):
            controller = controllers[x]
            event = controller.poll()
            if self.last_events[x] != event:
                self.last_events[x] = event
                return event

        return Event.NONE