""" Base class for joysticks """

from metafiddler.input_events import InputEvent

class GamepadInterface():
    # PLAYER BUTTONS
    # -----------------------------------------------------------------------------
    bindings = {
        "a": {"return": InputEvent.PLAYLIST_A},
        "b": {"return": InputEvent.PLAYLIST_B},
        "x": {"return": InputEvent.PLAYLIST_X},
        "y": {"return": InputEvent.PLAYLIST_Y},
        "left": {"return": InputEvent.NEXT},
        "right": {"return": InputEvent.SEEK_FORWARD},
        "start": {"return": InputEvent.PLAY},
        "select": {"return": InputEvent.STOP},
        "shoulder_l": {"return": InputEvent.SEEK_FORWARD},
        "shoulder_r": {"return": InputEvent.SEEK_BACK},

    }

    @classmethod
    def print_bindings(cls):
        print("""
       Seek back                                     Seek forward
     ╔════════════╗                                 ╔════════════╗
┌────╜────────────╙─────────────────────────────────╜────────────╙─────╖
│        vol up                                Playlist X              ▒
│         ╔══╗                                    ╭──╮                 ▒
│         ║  ║                                    │  │                 ▒
│      ╔══╝  ╚══╗                             ╭──╮╰──╯╭──╮             ▒
│ Prev ║        ║ Next            Playlist Y  │  │    │  │ Playlist A  ▒
│      ╚══╗  ╔══╝         ╭──╮     ╭──╮       ╰──╯╭──╮╰──╯             ▒
│         ║  ║            ╰──╯     ╰──╯           │  │                 ▒
│         ╚══╝            Stop      Play          ╰──╯                 ▒
│        vol dn                                Playlist B              ▒
│                                                                      ▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒""")