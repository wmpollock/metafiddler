# I'm not sure how necessary all this is but after looking at
# my excpetionally platform-specific joystick alternatives
# and thinking of future use cases I decided to abstract this
# I'm sure not quite enough.

# I mean, this could be REST or captive KBD or who knows.
# Input however should be nonblocking.
import metafiddler.controller_implementation.windows_keyboard
import metafiddler.controller_implementation.windows_usb_joystick
import metafiddler.event

# Maybe debouncing here is the more humane thing to do?  Of course it is...
last_events = [metafiddler.event.NONE, metafiddler.event.NONE]

controllers = [
    metafiddler.controller_implementation.windows_keyboard,
    metafiddler.controller_implementation.windows_usb_joystick
]

def init():
    global last_event
    global controllers
    for controller in controllers:
        controller.init()


def poll():
    global last_event
    global controllers
    #for controller in controllers:
    for x in range(len(controllers)):
        controller = controllers[x]
        event = controller.poll()
        if last_events[x] != event:
            last_events[x] = event
            return event

    return metafiddler.event.NONE