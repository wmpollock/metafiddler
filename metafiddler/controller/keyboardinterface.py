from metafiddler.events.input import Event
from tabulate import tabulate

class KeyboardInterface:

    bindings = {
        's': {
            "return":  Event.STOP,
        },
        'q': {
            "return":  Event.STOP,
        },

        'p': {
            "return":  Event.PLAY,
        }, 
        ', ': {
            "return":  Event.SEEK_BACK,
        }, 
        '.': {
            "return":  Event.SEEK_FORWARD,
        },
        # PLAYLISTS
        # -----------------
        'a': {
            "return":  Event.PLAYLIST_A,
        },
        'b': {
            "return":  Event.PLAYLIST_B,
        },
        'x': {
            "return":  Event.PLAYLIST_X,
        },
        'y': {
            "return":  Event.PLAYLIST_Y,
        },

        'w': {
            "return":  Event.GO_SOURCE,
        }, 

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
        
        print(tabulate(table, tablefmt="grid") )
