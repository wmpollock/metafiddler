""" Abstract class to base keyboard controllers

It turns out that having a generic set of interfaces is /amazingly/ complicated.

First: cross platform is /maybe/ a thing for some vectors.  Problems I've had
with cross-platform libraries:
    * (most): aren't cross-platform.  Much of the canon is linuxish OR windows.
    * inputs: cross platform but out of the but the gamepad blocks.
    There's a windows-only fix for that. Blocking is no go so yeet especially since I had windows
    dialed already standalone.
        I also had mixed experiences needing root/adding groups.  Even after adding groups
    I needed root in my xterm: I shouldn't have needed a reboot or anything.
    * pygame: needs a 1x1 window to be active; there are headless kludges but that's not where I
    want to be.
    * piborg/gamepad: wanted this one to work /SO BADLY/ because it had everything...
    except easy handling for my controller.  Benchmarks threw error :/

Other contenders:
https://github.com/justengel/pygamepad
https://pypi.org/project/python-uinput/ - low level
https://pypi.org/project/gamepadinfo/ - kitchen sink


"""

from tabulate import tabulate

class ControllerInterface:
    """ Abstract input interface class """
    bindings = {}

    def print_bindings(self):
        """ Display the bindings for a given key """
        table = []
        bindings = self.bindings
        for key in bindings.keys():
            # Haha, since we use the labels I guess we don't need a dictionary to look these up (yikes...)

            if "description" in bindings[key]:
                label = bindings[key]["description"]
            else:
                label = key

            # ?print("\t%-15s %s" %(label + ":", bindings[key]["return"]))
            table.append([label, bindings[key]["return"].description])

        print(tabulate([["Keyboard mapping"]], tablefmt="github"))

        print(tabulate(table, tablefmt="grid"))

    def poll(self):
        """ Interface class """
        raise NotImplementedError()
