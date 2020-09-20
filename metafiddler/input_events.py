"""
We need labels to use and we need constants that may or may not mean
anything.  This intersection seems as good a place as any to pile
labels to misuse in configuration map dumps.
"""

import re

class EventType: # pylint: disable=too-few-public-methods
    """ Individual event types """

    PLAYLIST = "playlsit"

    def __init__(self, description, event_id, event_type=""):
        self.event_id = event_id
        self.description = description
        self.type = event_type

    def __str__(self):
        self.event_id

class InputEvent: # pylint: disable=too-few-public-methods
    """ Class containing input events """
    NONE = EventType("Nothing happened.", "nothing")

    STOP = EventType("Stop playing current track", "stop")
    PLAY = EventType("Resume playing the current track", "play")
    NEXT = EventType("Play next page", "next")
    PREVIOUS = EventType("Play the previous page", "previous")

    SEEK_FORWARD = EventType("Fast forward in track", "seek_forward")
    SEEK_BACK = EventType("Seek back in track", "seek_back")

    VOLUME_UP = EventType("Volume up", "volume_up")
    VOLUME_DOWN = EventType("Volume down", "volume_down")

    # These playlist_ids are passed through checkes for playlist_id
    PLAYLIST_A = EventType("Add to playlist 'A'", "playlist_a", "playlist")
    PLAYLIST_B = EventType("Add to playlist 'B'", "playlist_b", "playlist")
    PLAYLIST_X = EventType("Add to playlist 'X'", "playlist_x", "playlist")
    PLAYLIST_Y = EventType("Add to playlist 'Y'", "playlist_y", "playlist")

    GO_SOURCE = EventType("Open source webpage","open_web")


    @classmethod
    def events(cls):
        """ List all defined events """

        return list(map(lambda x: cls.__dict__[x],
                        filter(lambda x: re.match(r'^[A-Z]+\w+$', x), cls.__dict__.keys())
                        )
        )
