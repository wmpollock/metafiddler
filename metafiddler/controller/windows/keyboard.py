"""Keyboard controller with specific windows-mappings.

IDK, now having the "standard" solution maybe this is not
entirely necessary for my use cases (GitBash)

"""


import logging
import sys
# https://stackoverflow.com/questions/9602811/how-to-tell-pylint-to-ignore-certain-imports
import msvcrt # pylint: disable=import-error
from metafiddler.input_events import InputEvent
from metafiddler.controller.keyboardinterface import KeyboardInterface


class Keyboard(KeyboardInterface):
    """Windows-based keyboard events"""

    def __init__(self):
        if not sys.stdin.isatty():
            logging.critical(
                "FATAL: this process is not a terminal.  Perhaps you need to prefix with winpty."
            )
            sys.exit()

        self.bindings.update(
            {
                # Well, IDK how I feel about using CHRs for BYTEs right about now
                # but they came out of the two-step polling process pretty tidy
                # as chars and I kinda like 'em.
                b"\000"
                + b"M": {
                    "return": InputEvent.NEXT,
                    # "description": "arrrow-forward"
                    "description": "→",
                },
                b"\000"
                + b"K": {
                    "return": InputEvent.PREVIOUS,
                    # "description": "arrow-back"
                    "description": "←",
                },
                b"\000"
                + b"H": {
                    "return": InputEvent.VOLUME_UP,
                    # "description": "arrow-up"
                    "description": "↑",
                },
                b"\000"
                + b"P": {
                    "return": InputEvent.VOLUME_DOWN,
                    # "description": "arrow-down"
                    "description": "↓",
                },
                # I don't get this second set but winpty seemed to need it?  Seems crass.
                b"\xe0"
                + b"M": {
                    "return": InputEvent.NEXT,
                    # "description": "arrrow-forward"
                    "description": "→",
                },
                b"\xe0"
                + b"K": {
                    "return": InputEvent.PREVIOUS,
                    # "description": "arrow-back"
                    "description": "←",
                },
                b"\xe0"
                + b"H": {
                    "return": InputEvent.VOLUME_UP,
                    # "description": "arrow-up"
                    "description": "↑",
                },
                b"\xe0"
                + b"P": {
                    "return": InputEvent.VOLUME_DOWN,
                    # "description": "arrow-down"
                    "description": "↓",
                },
                # escape: may not want to print this bad boi
                chr(27): {"return": InputEvent.STOP, "description": "escape"},
            }
        )

        self.print_bindings()

    def poll(self):
        """See if there is any input on this device"""
        if not sys.stdin.isatty():
            logging.critical(
                "FATAL: this process is not a terminal.  Perhaps you need to prefix with winpty."
            )
            sys.exit()

        # Second one necessary for winpty
        keycode_signals = [b"\000", b"\xe0"]
        try:
            if msvcrt.kbhit():

                ch = msvcrt.getch()

                # Arrow keys have a prefix
                if ch in keycode_signals:
                    x = msvcrt.getch()
                    key = ch + x
                elif ch:
                    key = ch.decode("utf-8")
                else:
                    logging.error("WHAT?!?  No key for my key?!?")

                if key in self.bindings:
                    return self.bindings[key]["return"]
        except KeyboardInterrupt:
            print("Yeet then")
            sys.exit(1)  # ?

        return InputEvent.NONE
