"""Keyboard controller with UNIX-y leanings

This is the standard python solution for reading keyboads except
 for (some)? form of windows which is of course lulzy

"""
import fcntl
import os
import termios
import sys

from metafiddler.input_events import InputEvent
from metafiddler.controller.keyboardinterface import KeyboardInterface

ARROW_PREFIX =  "\x1b["

# Thanks, FAQ:
# https://docs.python.org/2/faq/library.html#how-do-i-get-a-single-keypress-at-a-time

class Keyboard(KeyboardInterface):
    def __init__(self):
        fd = self.fd = sys.stdin.fileno()

        self.oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        self.oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

        self.bindings.update(
            {
                ARROW_PREFIX + "C": {
                    "return": InputEvent.NEXT,
                    # "description": "arrrow-forward"
                    "description": "→",
                },
                ARROW_PREFIX + "D": {
                    "return": InputEvent.PREVIOUS,
                    # "description": "arrow-back"
                    "description": "←",
                },
                ARROW_PREFIX + "A": {
                    "return": InputEvent.VOLUME_UP,
                    # "description": "arrow-up"
                    "description": "↑",
                },
                ARROW_PREFIX + "B": {
                    "return": InputEvent.VOLUME_DOWN,
                    # "description": "arrow-down"
                    "description": "↓",
                },
            }
        )

        self.print_bindings()
        print(self.bindings)

    def __del__(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

    def poll(self):
        """See if there is any input on this device"""
        try:
            c = sys.stdin.read(1)

            if c:
                
                char = repr(c)
                print(f"CHAR! {c} {char}")
                # CONTROLLL SEQUEEENCE
                if c == "\x1b":
                    esc = sys.stdin.read(1)
                    arrow = sys.stdin.read(1)
                    lookup = c + esc + arrow
                    if lookup in self.bindings:
                        return self.bindings[lookup]["description"]
                
                if char in self.bindings:
                    return self.bindings[char]["return"]

        except IOError:
            pass

        return InputEvent.NONE
