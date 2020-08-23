from metafiddler.input_events import InputEvent
from tabulate import tabulate


class KeyboardInterface:

    bindings = {
        "s": {"return": InputEvent.STOP,},
        "q": {"return": InputEvent.STOP,},
        "p": {"return": InputEvent.PLAY,},
        ", ": {"return": InputEvent.SEEK_BACK,},
        ".": {"return": InputEvent.SEEK_FORWARD,},
        # PLAYLISTS
        # -----------------
        "a": {"return": InputEvent.PLAYLIST_A,},
        "b": {"return": InputEvent.PLAYLIST_B,},
        "x": {"return": InputEvent.PLAYLIST_X,},
        "y": {"return": InputEvent.PLAYLIST_Y,},
        "w": {"return": InputEvent.GO_SOURCE,},
    }

    def print_bindings(self):
        table = []
        bindings = self.bindings
        for key in bindings.keys():
            # Haha, since we use the labels I guess we don't need a dictionary to look these up (yikes...)

            if "desc" in bindings[key]:
                label = bindings[key]["desc"]
            else:
                label = key

            # ?print("\t%-15s %s" %(label + ":", bindings[key]["return"]))
            table.append([label, bindings[key]["return"]])

        print(tabulate([["Keyboard mapping"]], tablefmt="github"))

        print(tabulate(table, tablefmt="grid"))
