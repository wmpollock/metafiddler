import msvcrt
import metafiddler.event
import sys

def init():
    if not sys.stdin.isatty():
        print("FATAL: this process is not a termain.  Perhaps you need to run winpty?")
        exit()

    # If this print is janky perhaps you need to 
    # setx PYTHONIOENCODING utf-8
    # Seems you Can't Just Do That for Friends
    print("Keyboard mapping:\n",
        "Mapping:\n",
        # "🡆     - next\n",
        # "🡄     - prev\n",
        # "🡅     - volume up\n",
        # "🡇     - volume down\n",
        # Fancypants arrows don't work in WinPTY?!?
        "[left]      - next\n",
        "[right]     - prev\n",
        "[up]        - volume up\n",
        "[down]      - volume down\n\n",
        
        "s|ESC - stop\n",
        "p     - start\n",
        "a     - Playlist A\n",
        "b     - Playlist B\n"
        )

def poll():
    keycode_signals = [b'\000', b'\xe0']

    if msvcrt.kbhit():
        key = msvcrt.getch()

        if key in keycode_signals:
            # apperently its a two-banger?
            key = msvcrt.getch()
            # I mean, I guess key is as good as any?
            if key == b'M':
                # 🡆 - next
                return(metafiddler.event.NEXT)
            elif key == b'K':
                # 🡄 - prev
                return(metafiddler.event.PREVIOUS)
            elif key == b'H':
                # 🡅 - volume up
                return(metafiddler.event.VOLUME_UP)
            elif key == b'P':
                # 🡇 - volume down
                return(metafiddler.event.VOLUME_DOWN)
        
        if (ord(key) == 27 or
            key == b's'):
            #  s|ESC - stop
            return(metafiddler.event.STOP)
        elif key == b'p':
            #   p - start
            return(metafiddler.event.PLAY) 
        elif key == b'a':         
            #   a - Playlist A
            return(metafiddler.event.PLAYLIST_A)
        elif key == b'a':         
            #   b - Playlist B
            return(metafiddler.event.PLAYLIST_B)

    return metafiddler.event.NONE

if __name__ == "__main__":
    last_r = ""
    while 1:
        r = poll()
        if last_r != r:
            print("Event!", r)
            last_r = r