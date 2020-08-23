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
                "\x1b"
                + "["
                + "C": {
                    "return": InputEvent.NEXT,
                    # "desc": "arrrow-forward"
                    "desc": "→",
                },
                "\x1b"
                + "["
                + "C": {
                    "return": InputEvent.NEXT,
                    # "desc": "arrrow-forward"
                    "desc": "→",
                },
                "\x1b"
                + "["
                + "D": {
                    "return": InputEvent.PREVIOUS,
                    # "desc": "arrow-back"
                    "desc": "←",
                },
                "\x1b"
                + "["
                + "A": {
                    "return": InputEvent.VOLUME_UP,
                    # "desc": "arrow-up"
                    "desc": "↑",
                },
                "\x1b"
                + "["
                + "B": {
                    "return": InputEvent.VOLUME_DOWN,
                    # "desc": "arrow-down"
                    "desc": "↓",
                },
            }
        )

        self.print_bindings()

    def __del__(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

    def poll(self):
        """See if there is any input on this device"""
        try:
            c = sys.stdin.read(1)
            if c:
                char = repr(c)
                # CONTROLLL SEQUEEENCE
                if c == "\x1b":
                    esc = sys.stdin.read(1)
                    arrow = sys.stdin.read(1)
                    lookup = c + esc + arrow
                    if lookup in self.bindings:
                        return self.bindings[lookup]["desc"]
                elif char in self.bindings:
                    return char

        except IOError:
            pass

        return InputEvent.NONE
