""" Abstract class to base keyboard controllers on """

from tabulate import tabulate
from metafiddler.input_events import InputEvent

class KeyboardInterface:
    """ Abstract keyboard class """
    bindings = {
        "s": {"return": InputEvent.STOP},
        "q": {"return": InputEvent.STOP},
        "p": {"return": InputEvent.PLAY},
        ",": {"return": InputEvent.SEEK_BACK},
        ".": {"return": InputEvent.SEEK_FORWARD},
        # PLAYLISTS
        # -----------------
        "a": {"return": InputEvent.PLAYLIST_A},
        "b": {"return": InputEvent.PLAYLIST_B},
        "x": {"return": InputEvent.PLAYLIST_X},
        "y": {"return": InputEvent.PLAYLIST_Y},
        "w": {"return": InputEvent.GO_SOURCE},
    }

    def print_bindings(self):
        """ Display the bindings for a given key """
        table = []
        bindings = self.bindings
        for key in bindings:
            # Haha, since we use the labels I guess we don't need a dictionary to look these up (yikes...)

            if "description" in bindings[key]:
                label = bindings[key]["description"]
            else:
                label = key

            # ?print("\t%-15s %s" %(label + ":", bindings[key]["return"]))
            table.append([label, bindings[key]["return"].description])

        print(tabulate([["Controller mapping"]], tablefmt="github"))

        print(tabulate(table, tablefmt="grid"))
