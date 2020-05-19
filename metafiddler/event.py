# We need labels to use and we need constants that may or may not mean
# anything.  This intersection seems as good a place as any to pile
# labels to misuse in configuration map dumps.

# Some constants
NONE = ''
STOP = 'stop'
PLAY = 'play'

NEXT = 'next track'
PREVIOUS = 'previous track'

SEEK_FORWARD = 'fast forward'
SEEK_BACK = 'rewind'

VOLUME_UP = 'LOUDER'
VOLUME_DOWN = 'quieter'

# These values are passed through checkes for playlist_id
PLAYLIST_A = 'playlist_a'
PLAYLIST_B = 'playlist_b'
PLAYLIST_X = 'playlist_x'
PLAYLIST_Y = 'playlist_y'

GO_SOURCE = 'Open source webpage'

# And then you go, man, why didn't I just do something sensible when I
# created this in the damnedfirstplace and maybe its not too late yet.
# But it is.
events = [
    NONE, 
    STOP, PLAY, 
    NEXT, PREVIOUS, 
    SEEK_FORWARD, SEEK_BACK,
    VOLUME_UP, VOLUME_DOWN,
    PLAYLIST_A, PLAYLIST_B, PLAYLIST_X, PLAYLIST_Y
]


# Course then you get all sporty and want to pass the event as a value and then
# changing it to a description doesn't fit athat 
addl_desc = {
    'playlist_a': 'Add to playlist A',
    'playlist_b': 'Add to playlist B',
    'playlist_x': 'Add to playlist X',
    'playlist_y': 'Add to playlist Y'
}



# And then of course you need a dangol event mangler to handle that non-seeennnnsee
def describe(e):
    if e in addl_desc:
        return(addl_desc[e])
    else:
        return(e)
