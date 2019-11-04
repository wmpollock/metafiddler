# I'm not sure how necessary all this is but after looking at
# my excpetionally platform-specific joystick alternatives
# and thinking of future use cases I decided to abstract this
# I'm sure not quite enough.

# I mean, this could be REST or captive KBD or who knows.
# Input however should be nonblocking.
import controllerimplementation.windows as controller

def poll():
    return(controller.poll())