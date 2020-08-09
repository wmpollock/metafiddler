# I'm not sure how necessary all this is but after looking at
# my excpetionally platform-specific joystick alternatives
# and thinking of future use cases I decided to abstract this
# I'm sure not quite enough.

controllers = []

hasKeyboard = False

from metafiddler.events.input import Event

import metafiddler.controller.keyboard
controllers.append(metafiddler.controller.keyboard.Keyboard())

# try:
#    import metafiddler.controller.windows.usb_joystick
#    controllers.append(metafiddler.controller.windows.usb_joystick.Joystick())
# except:
#     print("Can't add Windows USB Joystick")
#     pass



class Input:
    # Maybe debouncing here is the more humane thing to do?  Of course it is...
    last_events = [Event.NONE, Event.NONE]

    def __init__(self):
        if len(controllers) == 0:
            print("FATAL: no input controllers found.")
            exit(1)

    def poll(self):
        #for controller in controllers:
        for x in range(len(controllers)):
            controller = controllers[x]
            event = controller.poll()
            if self.last_events[x] != event:
                self.last_events[x] = event
                return event

        return Event.NONE