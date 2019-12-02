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

import os
# Needs to be before we invoke pygame because thanks, pygame, IHI.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import logging
from metafiddler.config import MufiConfig
import metafiddler.controller
import metafiddler.event 
from metafiddler.page import MufiPage
import multiprocessing
import os.path 
import pygame
import sys
import webbrowser

# Starts at 1K, w/o it the pickling of the object is a no, go: maybe
# we got something else bad in here...
sys.setrecursionlimit(10000)

# Command line promises made and undelivered:
# need to pass --config_file down into metafiddler.config

def get_next(queue, page):
    #queue.put(page.provision())
     r = page.provision()
     queue.put(r, False, 2)
    

def main():
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    metafiddler.controller.init()
    metafiddler.mechanise.init()
    config = MufiConfig()
    
    logging.info("Playlist A: " + config.playlist_title('playlist_a'))
    logging.info("Playlist B: " + config.playlist_title('playlist_b'))

    current_page = MufiPage(config.current_page)
    
    logging.debug("Setting up current page")
    current_page.provision()
    
    # Other things:
    # #"published_parsed": entry.published_parsed,
    #        +    "audio_file_url": url,
    #        -    "audio_source_url": entry.link
    
  
    done = False

    while not(done):

        # Download the next page while we're listening to this one so we're 
        # good to go.
        # --------------------------------------------------------------------
        next_page = current_page.links["newer"]
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=get_next, args=(queue, next_page))
        process.start()
        # Yeahhhh, we're potentially writing what we just read but it keeps
        # current current, ya know?
        config.current_page = current_page.audio_source_url
        config.save()

        # Start playing
        current_page.song.play_title()
        current_page.song.play()

        # We're going to loop we get an explicit action, send to 
        # playlist or whatever.  Since we're curating we don't want to
        # just keep rolling through.
        song_actioned = False
        input_prompted = False
        while current_page.song.playing() and not song_actioned:
            if not (current_page.song.playing() or input_prompted):
                input_prompted = True
                logging.info("Waiting for user for input.")

            # This event stacking makes it seem like we're not going to deal
            # with +1 events and, um, yes, wait for the next poll and 
            # pop them off your stack or something.
            e = metafiddler.controller.poll()

            # ** I really wanted to put all these into a magnificent map but python
            # does not have a multiline lambda and IDK if busting them functions is
            # more sensible?
            
            if not e == metafiddler.event.NONE:
                logging.info("EVENT: " + e)

            if e == metafiddler.event.STOP:
                current_page.song.stop()
                # Not really on this but since we're going to come back here after we
                # bail, should be A-OK.
                song_actioned = True
                done = True
                
            # Kind of useless w/o STOP =~ /pause??
            elif e == metafiddler.event.PLAY:
                # Maybe this should do something if its not playing?
                current_page.song.play()

            elif e == metafiddler.event.NEXT:
                pygame.mixer.music.fadeout(100)
                song_actioned = True

            elif e == metafiddler.event.PREVIOUS:
                # TODO: variant behavior/naming.  We should also
                # have a back navigationally.  There should be symmetry
                # between seek/positional and navigational controls. 
                # Back = "Seek back" sounds maybe sensible?
                pygame.mixer.music.fadeout(100)
                song_actioned = True

            elif e == metafiddler.event.VOLUME_UP:
                v = pygame.mixer.music.get_volume()
                if v < 1:
                    pygame.mixer.music.set_volume(v + .1)

            elif e == metafiddler.event.VOLUME_DOWN:
                v = pygame.mixer.music.get_volume()
                if v > 0:
                    pygame.mixer.music.set_volume(v - .1)
 
            elif e == metafiddler.event.PLAYLIST_A:
                pygame.mixer.music.fadeout(100)
                current_page.song.playlist_add(config.playlist_id('playlist_a'))
                song_actioned = True
                
            elif e == metafiddler.event.PLAYLIST_B:
                pygame.mixer.music.fadeout(100)
                current_page.song.playlist_add(config.playlist_id('playlist_b'))
                song_actioned = True
            
            elif e == metafiddler.event.SEEK_BACK:
                p = pygame.mixer.music.get_pos()
                if p > 100:
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.play()
                    
                    # Says [https://www.pygame.org/docs/ref/music.html]
                    #   For absolute positioning in an MP3 file, first call rewind()
                    # But this is kind of nonsense because if when you fire this it
                    # ends up going to some not-this number and then bailing :/
                    #pygame.mixer.music.set_pos(p-100)
                    #print("Now at ", pygame.mixer.music.get_pos())

            elif e == metafiddler.event.SEEK_FORWARD:
                if current_page.song.playing():
                    # Fortunately only mp3s as seek is conditional on format :O
                    pygame.mixer.music.set_pos(100)

            elif e == metafiddler.event.GO_SOURCE:
                webbrowser.open(current_page.audio_source_url, new=2)
        # This is the resolved end page which is already provisioned...
        next_page = queue.get(timeout=15)
        process.join()
        if e == metafiddler.event.PREVIOUS:
            current_page = current_page.links["older"]
            current_page.provision()
        else:
            current_page = next_page
        

if __name__ == '__main__':
    main()