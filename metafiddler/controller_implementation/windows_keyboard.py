import msvcrt
import metafiddler.event
import sys
import logging


def init():
    if not sys.stdin.isatty():
        logging.critical("FATAL: this process is not a terminal.  Perhaps you need to prefix with winpty.")
        exit()

    # If this print is janky perhaps you need to 
    # setx PYTHONIOENCODING utf-8
    # Seems you Can't Just Do That for Friends
    logging.info("\n".join(
        ["Keyboard mapping:",
        
        # "🡆     - next",
        # "🡄     - prev",
        # "🡅     - volume up",
        # "🡇     - volume down",
        # Fancypants arrows don't work in WinPTY?!?
        "\t[left]  - next",
        "\t[right] - prev",
        "\t[up]    - volume up",
        "\t[down]  - volume down",
        
        "\ts|ESC  - stop",
        "\tp      - start",
        "\ta      - Playlist A",
        "\tb      - Playlist B"
        ])
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
            logging.debug("Event:" + r)
            last_r = r