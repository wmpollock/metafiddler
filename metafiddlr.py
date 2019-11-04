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
import multiprocessing
import pygame
import pprint 


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

def get_next(queue, page):
    queue.put(page.provision(subdir="Metafilter"))

def main():
    done = 0

    metafiddler.controller.init()
    
    current_page = MufiPage('file:sample/8716.html')
    print(current_page)
    print("Seeing up current page")
    current_page.provision(subdir="MetaFiddler")
    print(current_page)
    
    # Other things:
    # #"published_parsed": entry.published_parsed,
    #        +    "audio_file_url": url,
    #        -    "audio_source_url": entry.link


    while not(done):

        # Background this     
        next_page = current_page.links["newer"]
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=get_next, args=(queue, next_page))
        process.start()

        # Start playing
        print("Playing...")
        current_page.song.play()

        while current_page.song.playing():
            # This event stacking makes it seem like we're not going to deal
            # with +1 events and, um, yes, wait for the next poll and 
            # pop them off your stack or something.
            e = metafiddler.controller.poll()

             # Debounce event
            if e == metafiddler.event.STOP:
                print("-> Stop [psyche!  pause!]!")
                current_page.song.pause()
                
            elif e == metafiddler.event.PLAY:
                current_page.song.play()

            elif e == metafiddler.event.NEXT:
                print("NEXT")
            elif e == metafiddler.event.PREVIOUS:
                print("PREVIOUS")
            elif e == metafiddler.event.VOLUME_UP:
                v = pygame.mixer.music.get_volume()
                if v < 1:
                    pygame.mixer.music.set_volume(v + .1)

            elif e == metafiddler.event.VOLUME_DOWN:
                v = pygame.mixer.music.get_volume()
                if v > 1:
                    pygame.mixer.music.set_volume(v - .1)

 
            elif e == metafiddler.event.PLAYLIST_A:
                print("PYLIST AAAAA")
           
            elif e == metafiddler.event.PLAYLIST_B:
                print("PLAYLIsT BBBBBB")

            # Ticking jacks our kbd/joy scane            
            #pygame.time.Clock().tick(.25)

    #         # Save state
            # Backup/propagate state to remote

            # At tis point its ended without us actioning?
        current_page = queue.get()
        process.join()
        print(current_page)
        exit()

if __name__ == '__main__':
    main()            