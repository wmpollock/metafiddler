#  __  __      _         __ _     _     _ _
# |  \/  | ___| |_ __ _ / _(_) __| | __| | | ___ _ __
# | |\/| |/ _ \ __/ _` | |_| |/ _` |/ _` | |/ _ \ '__|
# | |  | |  __/ || (_| |  _| | (_| | (_| | |  __/ |
# |_|  |_|\___|\__\__,_|_| |_|\__,_|\__,_|_|\___|_|
#
# ----------------------------------------------------------------------------
# Desperately cruising the desolate information superhighway for tunes, man...
# Tunes.
#
# Pollock, 2019
# ============================================================================

import logging
from metafiddler.config import MufiConfig
import metafiddler.controller
import metafiddler.event 
from metafiddler.page import MufiPage
import multiprocessing
import os
import os.path 
import pygame
import pprint 


# I mean, thx and all, but....
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Command line promises made and undelivered:
# need to pass --config_file down into metafiddler.config

def get_next(queue, page):
    queue.put(page.provision(subdir="Metafilter"))

def main():
    logging.basicConfig(level=logging.DEBUG)

    done = 0

    metafiddler.controller.init()
    metafiddler.mechanise.init()
    config = MufiConfig()

#    print(config)
    
    logging.info("\nPlaylist A: " + config.playlist_title('playlist_a'))
    #logging.info("Playlist A ID:", config.playlist_id('playlist_a'))
    logging.info("\nPlaylist B: " + config.playlist_title('playlist_b'))

    current_page = MufiPage(config.current_page)
    
    logging.debug("Setting up current page")
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
        
        logging.debug("Playing title read")
        current_page.song.play_title()
        # Start playing
        logging.info("Playing...")
        current_page.song.play()


        # We're going to loop we get an explicit action, send to 
        # playlist or whatever.  Since we're curating we don't want to
        # just keep rolling through.
        song_actioned = 0
        while current_page.song.playing() or not song_actioned:
            # This event stacking makes it seem like we're not going to deal
            # with +1 events and, um, yes, wait for the next poll and 
            # pop them off your stack or something.
            e = metafiddler.controller.poll()

             # Debounce event
            if e == metafiddler.event.STOP:
                # W@ M8?!?
                # logging.info("-> Stop [psyche!  pause!]!")
                # current_page.song.pause()
                logging.info("STOP!")
                current_page.song.stop()
                # Not really on this but since we're going to come back here after we
                # bail, should be A-OK.
                song_actioned = 1
                done = 1
                
            # Kind of useless w/o STOP =~ /pause??
            elif e == metafiddler.event.PLAY:
                # Maybe this should do something if its not playing?
                current_page.song.play()

            elif e == metafiddler.event.NEXT:
                logging.info("NEXT")
                pygame.mixer.music.fadeout(100)
                song_actioned = 1


            elif e == metafiddler.event.PREVIOUS:
                logging.info("PREVIOUS")
                song_actioned = 1

            elif e == metafiddler.event.VOLUME_UP:
                logging.info("Volume up")
                v = pygame.mixer.music.get_volume()
                if v < 1:
                    pygame.mixer.music.set_volume(v + .1)

            elif e == metafiddler.event.VOLUME_DOWN:
                logging.info("Volume down")
                v = pygame.mixer.music.get_volume()
                if v > 0:
                    pygame.mixer.music.set_volume(v - .1)
 
            elif e == metafiddler.event.PLAYLIST_A:
                pygame.mixer.music.fadeout(100)
                current_page.song.playlist_add(config.playlist_id('playlist_a'))
                song_actioned = 1
                
            elif e == metafiddler.event.PLAYLIST_B:
                pygame.mixer.music.fadeout(100)
                current_page.song.playlist_add(config.playlist_id('playlist_b'))
                song_actioned = 1
                

        current_page = queue.get()
        process.join()
        logging.debug(current_page)

if __name__ == '__main__':
    main()            