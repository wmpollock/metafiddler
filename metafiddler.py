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
from pygame import mixer, time

#import controller as controller
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

    appState['current_page'].get(extract = True, blocking = True, subdir = 'MetaFiddler')
    current_page = appState['current_page']
    current_page.song.generate_description()

    exit()

    # Some things we need for metafodder:
    # +  artist
    # +  title
    #   list_name
    #   path

    # Other things:
    # #"published_parsed": entry.published_parsed,
    #        +    "audio_file_url": url,
    #        -    "audio_source_url": entry.link

    
    lastEvent = ''
    done = 0

    # while not(done):
    #     appState['next_page'] = current_page.links[newer]
    #     # Provision our content for the next round
    #     appState['next_page'].get(appState['current_page']['newer']['href'], extract = True)
    #     pprint.pprint(appState)

    #     #while mixer.music.get_busy():
    #     while audio.playing
    #         # This event stacking makes it seem like we're not going to deal
    #         # with +1 events and, um, yes, wait for the next poll and 
    #         # pop them off your stack or something.
    #         e = controller.poll()

    #         # Debounce event
    #         if lastEvent != e:
    #             print(e)
    #             if e == event.STOP:
    #                 print("-> Stop!")
    #                 mixer.music.stop()
    #             #elif event == event.PLAY:
    #                 # Some higgedy about already playing
    #             lastEvent = e
    #         #time.Clock().tick(.25)

    #         # Advance prev <- current 
    #         # and pull/provision next
    #         # Save state
            # Backup/propagate state to remote

if __name__ == '__main__':
    main()            