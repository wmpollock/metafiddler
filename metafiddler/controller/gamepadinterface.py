""" Base class for joysticks """

from metafiddler.input_events import InputEvent


class GamepadInterface:
    """ Interface class for gamepads/joysticks """

    # PLAYER BUTTONS
    # -----------------------------------------------------------------------------
    bindings = {
        "a": InputEvent.PLAYLIST_A,
        "b": InputEvent.PLAYLIST_B,
        "x": InputEvent.PLAYLIST_X,
        "y": InputEvent.PLAYLIST_Y,
        "left": InputEvent.NEXT,
        "right": InputEvent.SEEK_FORWARD,
        "start": InputEvent.PLAY,
        "select": InputEvent.STOP,
        "shoulder_r": InputEvent.SEEK_FORWARD,
        "shoulder_l": InputEvent.SEEK_BACK,
        "up": InputEvent.VOLUME_UP,
        "down": InputEvent.VOLUME_DOWN,
        "left": InputEvent.PREVIOUS,
        "right": InputEvent.NEXT,
    }

    @classmethod
    def print_bindings(cls):
        print(
            """
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
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"""
        )
