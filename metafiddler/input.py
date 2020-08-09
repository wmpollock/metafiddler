# I'm not sure how necessary all this is but after looking at
# my excpetionally platform-specific joystick alternatives
# and thinking of future use cases I decided to abstract this
# I'm sure not quite enough.

# I mean, this could be REST or captive KBD or who knows.
# Input however should be nonblocking.
import metafiddler.controller.windows_keyboard
import metafiddler.controller.windows_usb_joystick
from metafiddler.events.input import Event

# TODO: feels janky, load from files mebbe?
controllers = [
   metafiddler.controller.windows_keyboard,
   metafiddler.controller.windows_usb_joystick
]

class Input:
    # Maybe debouncing here is the more humane thing to do?  Of course it is...
    last_events = [Event.NONE, Event.NONE]

    def __init__(self):
        for controller in controllers:
            controller.init()

    def poll(self):
        #for controller in controllers:
        for x in range(len(controllers)):
            controller = controllers[x]
            event = controller.poll()
            if self.last_events[x] != event:
                self.last_events[x] = event
                return event

        return Event.NONE