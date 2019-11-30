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

from metafiddler.config import MufiConfig
import metafiddler.controller
import metafiddler.event 
from metafiddler.page import MufiPage
import multiprocessing
import pygame
import pprint 

# Command line promises made and undelivered:
# need to pass --config_file down into metafiddler.config

def get_next(queue, page):
    queue.put(page.provision(subdir="Metafilter"))

def main():
    done = 0

    metafiddler.controller.init()
    config = MufiConfig()
    
    current_page = MufiPage(config.current_page)
    
    print("Setting up current page")
    current_page.provision(subdir="MetaFiddler")
    
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

        # Yeahhhh, we're potentially writing what we just read but it keeps
        # current current, ya know?
        config.current_page = current_page.audio_source_url
        config.save()
        
        print("Playing title read")
        current_page.song.play_title()
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
                # W@ M8?!?
                # print("-> Stop [psyche!  pause!]!")
                # current_page.song.pause()
                print("STOP!")
                current_page.song.stop()
                done = 1
                
            # Kind of useless w/o STOP =~ /pause??
            elif e == metafiddler.event.PLAY:
                # Maybe this should do something if its not playing?
                current_page.song.play()

            elif e == metafiddler.event.NEXT:
                print("NEXT")
                pygame.mixer.music.fadeout(100)

            elif e == metafiddler.event.PREVIOUS:
                print("PREVIOUS")

            elif e == metafiddler.event.VOLUME_UP:
                print("Volume up")
                v = pygame.mixer.music.get_volume()
                if v < 1:
                    pygame.mixer.music.set_volume(v + .1)

            elif e == metafiddler.event.VOLUME_DOWN:
                print("Volume down")
                v = pygame.mixer.music.get_volume()
                if v > 0:
                    pygame.mixer.music.set_volume(v - .1)
 
            elif e == metafiddler.event.PLAYLIST_A:
                print("Playlist A")
                current_page.song.playlist_add(config.playlist_a)
                pygame.mixer.music.fadeout(100)
                
            elif e == metafiddler.event.PLAYLIST_B:
                print("Playlist B")
                current_page.song.playlist_add(config.playlist_b)
                pygame.mixer.music.fadeout(100)

        current_page = queue.get()
        process.join()
        print(current_page)

if __name__ == '__main__':
    main()            