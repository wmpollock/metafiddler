"""
We need labels to use and we need constants that may or may not mean
anything.  This intersection seems as good a place as any to pile
labels to misuse in configuration map dumps.
"""


class EventType:
    """ Individual even types """
    
    PLAYLIST = "playlsit"

    def __init__(self, description, id="", type=""):
        self.id = id
        self.description = description
        self.type = type



class InputEvents:
    """ Class containing input events """
    NONE = EventType("Nothing happened.")
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

    GO_SOURCE = EventType("Open source webpage")

    # And then you go, man, why didn't I just do something sensible when I
    # created this in the damnedfirstplace and maybe its not too late yet.
    # But it is.
    events = [
        NONE,
        STOP,
        PLAY,
        NEXT,
        PREVIOUS,
        SEEK_FORWARD,
        SEEK_BACK,
        VOLUME_UP,
        VOLUME_DOWN,
        PLAYLIST_A,
        PLAYLIST_B,
        PLAYLIST_X,
        PLAYLIST_Y,
    ]


