import msvcrt
import metafiddler.event
import sys
import logging


bindings = {
    # Well, IDK how I feel about using CHRs for BYTEs right about now
    # but they came out of the two-step polling process pretty tidy
    # as chars and I kinda like 'em.
    b'\000' + b'M': {
			"return":  metafiddler.event.NEXT,
            "desc": "arrrow-forward"
		},
    b'\000' + b'K': {
			"return":  metafiddler.event.PREVIOUS,
            "desc": "arrow-back"
		},
    b'\000' + b'H': {
			"return":  metafiddler.event.VOLUME_UP,
            "desc": "arrow-up"
		},
    b'\000' + b'P': {
			"return":  metafiddler.event.VOLUME_DOWN,
            "desc": "arrow-down"
		},
    # escape: may not want to print this bad boi 
     chr(27):  {
			"return":  metafiddler.event.STOP,
            "desc": "escape"
		},
    's': {
			"return":  metafiddler.event.STOP,
		},
    'p': {
			"return":  metafiddler.event.PLAY,
		}, 
    'z': {
			"return":  metafiddler.event.SEEK_BACK,
		}, 
    'x': {
			"return":  metafiddler.event.SEEK_FORWARD,
		},
    'a': {
			"return":  metafiddler.event.PLAYLIST_A,
		},
    'b': {
			"return":  metafiddler.event.PLAYLIST_B,
		},
}

# TODO:  It'd be nicer to have each binding as a standard
# defintion:
# bindings = {
#     'x' => {
#         # The event should have its own description that we look up 
#         event => 
#     }
# }



def init():
    if not sys.stdin.isatty():
        logging.critical("FATAL: this process is not a terminal.  Perhaps you need to prefix with winpty.")
        exit()
    
    print("Keyboard mapping:")
    for key in bindings.keys():
        # Haha, since we use the labels I guess we don't need a dictionary to look these up (yikes...)
        
        if "desc" in bindings[key]:
            label = bindings[key]["desc"]
        else:
            label = key

        print("\t%-15s %s" %(label + ":", bindings[key]["return"]))
    
    
    # If this print is janky perhaps you need to 
    # setx PYTHONIOENCODING utf-8
    # Seems you Can't Just Do That for Friends
        
    

def poll():
    if not sys.stdin.isatty():
        logging.critical("FATAL: this process is not a terminal.  Perhaps you need to prefix with winpty.")
        exit()

    #keycode_signals = [b'\000', b'\xe0']
    keycode_signal = b'\000'

    if msvcrt.kbhit():
        
        ch = msvcrt.getch()
        #print(ch.decode("utf-8"))
        #if ch in keycode_signals:
        
        # Arrow keys have a prefix
        if ch == keycode_signal:
            key = ch + msvcrt.getch()
        else:
            key = ch.decode("utf-8")

        if key in bindings:
            return bindings[key]["return"]


    return metafiddler.event.NONE

if __name__ == "__main__":
    init()
    last_r = ""
    print("Polling...")
    while 1:
        r = poll()
        if not last_r == r:
            if r:
                print("Event:" + r)
            last_r = r