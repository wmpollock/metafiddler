""" Abstract class to base keyboard controllers on """

from tabulate import tabulate
from metafiddler.input_events import InputEvent


class ControllerInterface:
    """ Abstract input interface class """
    bindings = {}

    def print_bindings(self):
        """ Display the bindings for a given key """
        table = []
        bindings = self.bindings
        for key in bindings.keys():
            # Haha, since we use the labels I guess we don't need a dictionary to look these up (yikes...)

            if "desc" in bindings[key]:
                label = bindings[key]["desc"]
            else:
                label = key

            # ?print("\t%-15s %s" %(label + ":", bindings[key]["return"]))
            table.append([label, bindings[key]["return"].description])

        print(tabulate([["Keyboard mapping"]], tablefmt="github"))

        print(tabulate(table, tablefmt="grid"))
