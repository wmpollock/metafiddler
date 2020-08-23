#!/usr/bin/env PYGAME_HIDE_SUPPORT_PROMPT=hide python3
"""Play through Metafilter Music one song at a time"""
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

# Command line promises made and undelivered:
# need to pass --config_file down into metafiddler.config
import logging
import multiprocessing
import webbrowser
import sys

# Needs to be before we invoke pygame because thanks, pygame, IHI.
# rm'd -- IDK that the shebang line counts in Windows land, I think maybe no :/
#   but with this in place ZOMG how pylint complains.
import os



import pygame
from tabulate import tabulate

from metafiddler.config import MufiConfig
from metafiddler.input import Input
from metafiddler.input_events import InputEvent
from metafiddler.page import MufiPage
from metafiddler.speech import Speaker

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Starts at 1K, w/o it the pickling of the object is a no, go: maybe
# we got something else bad in here...
sys.setrecursionlimit(10000)

class Run: 
    def provision_next_page(self, page):
        """ Callback from fork to provision the next page """
        # queue.put(page.provision())
        next_page = page.provision()
        self.queue.put(next_page, False, 2)


    def __init__(self):
        """Pre-run configurations"""

        self.config = MufiConfig()

        self.speaker = Speaker(config)

        self.speaker.say("Setting up current page.")

        self.current_page = MufiPage(config, config.current_page)

        self.user_input = Input()

        print(
            tabulate(
                [
                    ["Playlist A: ", config.playlist_title("playlist_a")],
                    ["Playlist B: ", config.playlist_title("playlist_b")],
                    ["Playlist X: ", config.playlist_title("playlist_x")],
                    ["Playlist Y: ", config.playlist_title("playlist_y")],
                ],
                tablefmt="grid",
            )
        )

        logging.debug("Setting up speech utterances.")

        self.speaker.say("Setting up speech utterances.")
        for event in InputEvent.events:
            logging.debug("Preparing for event %s", event)
            self.speaker.prepare(InputEvent.description)

        logging.debug("Setting up current page")
        self.current_page.provision()
        
    def main(self):
        """Primary entrance point"""
        
        done = False

        while not done:
            # Download the next page while we're listening to this one so we're
            # good to go.
            # --------------------------------------------------------------------
            self.config.current_page_url= current_page.audio_source_url
            
            current_page = self.current_page
            song = current_page.song
            next_page = current_page.links["newer"]

            # Bust off a new process to handle provisioning the queue asynchronously
            self.queue = queue = multiprocessing.Queue()
            process = multiprocessing.Process(
                target=self.provision_next_page, args=(queue, next_page)
            )
            process.start()
            
            # Start playing
            song.play_title()
            song.play()

            # We're going to loop we get an explicit action, send to
            # playlist or whatever.  Since we're curating we don't want to
            # just keep rolling through.
            self.song_actioned = False
            input_prompted = False
            while song.playing() and not self.song_actioned:
                if not (song.playing() or input_prompted):
                    # May as well not burn (reporting) cycles.                    
                    input_prompted = True
                    logging.info("Waiting for user for input.")

                # This event stacking makes it seem like we're not going to deal
                # with +1 events and, um, yes, wait for the next poll and
                # pop them off your stack or something.
                try:
                    event = self.user_input.poll()
                except KeyboardInterrupt:
                    logging.info("Keyboard interrupt: exiting")
                    self.speaker.say("Keyboard interrupt: exiting")
                    sys.exit(1)
                    
                # ** I really wanted to put all these into a magnificent map but python
                # does not have a multiline lambda and IDK if busting them functions is
                # more sensible?

                if event and event != InputEvent.NONE:
                    logging.info("EVENT: %s", event)
                    self.speaker.say(event.description)
                    if event.type == EventType.PLAYLIST
                        self.playlist(event)
                    else:
                        self.event.event_id()

            # This is the resolved end page which is already provisioned...
            next_page = queue.get(timeout=15)
            process.join()
            if event == InputEvent.PREVIOUS:
                current_page = current_page.links["older"]
                current_page.provision()
            else:
                current_page = next_page


    def stop(self):
        self.current_page.song.stop()
        # Not really on this but since we're going to come back here after we
        # bail, should be A-OK.
        self.song_actioned = True
        self.done = True

    def play(self):
        # Maybe this should do something if its not playing?
        self.current_page.song.play()

    def next(self):
        pygame.mixer.music.fadeout(100)
        self.song_actioned = True

    def previous(self):
        # Back = "Seek back" sounds maybe sensible?
        pygame.mixer.music.fadeout(100)
        self.song_actioned = True

    @classmethod
    def volume_up(cls):
        volume = pygame.mixer.music.get_volume()
        if volume < 1:
            pygame.mixer.music.set_volume(volume + 0.1)

    @classmethod
    def volume_down(cls):
        volume = pygame.mixer.music.get_volume()
        if volume > 0:
            pygame.mixer.music.set_volume(volume - 0.1)

    def playlist(self, playlist_id):
        pygame.mixer.music.fadeout(100)
        if config.playlist_id(playlist_id):
            if not current_page.song.playlist_add(playlist_id):
                logging.info("Looks a bit sketchy: bailing")
                self.done = True
            # TODO: This should go into the appropriate playlist
            # subdirectory...?
        else:
            logging.warning(           
                "No playlist configured for that button in this config (%s)",
                playlist_id)
            
        self.song_actioned = True

    def seek_back(self):
        position = pygame.mixer.music.get_pos()
        if position > 100:
            pygame.mixer.music.rewind()
            pygame.mixer.music.play()

            # Says [https://www.pygame.org/docs/ref/music.html]
            #   For absolute positioning in an MP3 file, first call rewind()
            # But this is kind of nonsense because if when you fire this it
            # ends up going to some not-this number and then bailing :/
            # pygame.mixer.music.set_pos(p-100)
            # print("Now at ", pygame.mixer.music.get_pos())

    def seek_forward(self):
        if self.current_page.song.playing():
            # Fortunately only mp3s as seek is conditional on format :O
            pygame.mixer.music.set_pos(100)

    def open_source_page(self):
            webbrowser.open(current_page.audio_source_url, new=2)


if __name__ == "__main__":

    run = Run()
    run.main()
