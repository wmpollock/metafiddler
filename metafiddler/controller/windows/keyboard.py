import logging
from metafiddler.events.input import Event
import sys
from tabulate import tabulate


import msvcrt

class Keyboard(KeyboardInterrupt):

    def init():
        if not sys.stdin.isatty():
            logging.critical("FATAL: this process is not a terminal.  Perhaps you need to prefix with winpty.")
            exit()
        
        self.bindings.update({}
            # Well, IDK how I feel about using CHRs for BYTEs right about now
            # but they came out of the two-step polling process pretty tidy
            # as chars and I kinda like 'em.
            b'\000' + b'M': {
                "return":  Event.NEXT,
                # "desc": "arrrow-forward"
                "desc": "→"
            },
            b'\000' + b'K': {
                "return":  Event.PREVIOUS,
                # "desc": "arrow-back"
                "desc": '←'
            },
            b'\000' + b'H': {
                "return":  Event.VOLUME_UP,
                # "desc": "arrow-up"
                "desc": "↑"
            },
            b'\000' + b'P': {
                "return":  Event.VOLUME_DOWN,
                # "desc": "arrow-down"
                "desc": "↓"

            },

            # I don't get this second set but winpty seemed to need it?  Seems crass.
            b'\xe0' + b'M': {
                "return":  Event.NEXT,
                # "desc": "arrrow-forward"
                "desc": "→"
            },
            b'\xe0' + b'K': {
                "return":  Event.PREVIOUS,
                # "desc": "arrow-back"
                "desc": '←'
            },
            b'\xe0' + b'H': {
                "return":  Event.VOLUME_UP,
                # "desc": "arrow-up"
                "desc": "↑"
            },
            b'\xe0' + b'P': {
                "return":  Event.VOLUME_DOWN,
                # "desc": "arrow-down"
                "desc": "↓"
            },

            # escape: may not want to print this bad boi 
            chr(27):  {
                "return":  Event.STOP,
                "desc": "escape"
            },
        })

        self.print_bindings()        

    def poll():
        if not sys.stdin.isatty():
            logging.critical("FATAL: this process is not a terminal.  Perhaps you need to prefix with winpty.")
            exit()

        # Had this commented out in favor of the singleton which didn't catch Winpty I guess?
        keycode_signals = [b'\000', b'\xe0']
        #keycode_signal = b'\000'
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

                if key in bindings:
                    return bindings[key]["return"]
        except KeyboardInterrupt:
            raise


        return Event.NONE

if __name__ == "__main__":
    init()
    last_r = ""
    print("Polling...")
    while 1:
        r = poll()
        if not last_r == r:
            if r:
                print("Event:" + r)
            last_r = r