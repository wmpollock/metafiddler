#  __  __      _         __ _     _     _ _
# |  \/  | ___| |_ __ _ / _(_) __| | __| | | ___ _ __
# | |\/| |/ _ \ __/ _` | |_| |/ _` |/ _` | |/ _ \ '__|
# | |  | |  __/ || (_| |  _| | (_| | (_| | |  __/ |
# |_|  |_|\___|\__\__,_|_| |_|\__,_|\__,_|_|\___|_|
#

# Cruising the information superhighway for tunes, man.
# Tunes.
# Pollock, 2019

import os
import os.path 

# I mean, thx and all, but....
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import metafiddler.controller
import metafiddler.event 
from metafiddler.page import MufiPage

import pprint 
appState = {
    'current_page': MufiPage('file:sample/8716.html')
}

# {'artist': 'TheNegativeInfluence',
#  'audio_file_url': '//mefimusic.s3.amazonaws.com/Down%20a%20Hole.mp3',
#  'audio_source_url': 'http://music.metafilter.com/8716/Down-a-Hole',
#  'list_title': '.Evaluation Hopper',
#!!! THIS IS NOT THE SAME IN 
#  'mp3_localfile': 'C:\\Users\\Bill\\Music\\MetaFilter\\.Evaluation '
#                   'Hopper\\TheNegativeInfluence - Down a Hole.mp3',
#  'newer': {'href': 'https://music.metafilter.com/8717/It-Dont-Matter-Whos-First-In-Line'},
#  'older': {'href': 'https://music.metafilter.com/8715/Manhattan-Skyline'},
#  'title': 'Down a Hole'}

def main():
    lastEvent = ''
    done = 0


    print("Seeing up current page")
    appState['current_page'].provision(subdir="MetaFiddler")
    current_page = appState['current_page']


    # Other things:
    # #"published_parsed": entry.published_parsed,
    #        +    "audio_file_url": url,
    #        -    "audio_source_url": entry.link


    while not(done):

        # Background this     
        #appState['next_page'] = current_page.links[newer]
        #appState['next_page'].provision(subdir="MetaFiddler")
    
        current_page.song.play_title()
        # Start playing
        current_page.song.play()

    #     #while :
        while current_page.song.playing():
             # This event stacking makes it seem like we're not going to deal
             # with +1 events and, um, yes, wait for the next poll and 
             # pop them off your stack or something.
             e = metafiddler.controller.poll()

             # Debounce event
                 print(e)
                 if e == metafiddler.event.STOP:
                     print("-> Stop!")
                     mixer.music.stop()
                 #elif event == event.PLAY:
                     # Some higgedy about already playing
                 lastEvent = e
             #time.Clock().tick(.25)

             # Advance prev <- current 
    #         # and pull/provision next
    #         # Save state
            # Backup/propagate state to remote

        # At tis point its ended without us actioning?
        exit()

if __name__ == '__main__':
    main()            