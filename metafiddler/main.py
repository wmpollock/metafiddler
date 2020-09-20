""" Body of the metafiddler application """

import logging
import multiprocessing
import webbrowser
import sys

import pygame  #
from tabulate import tabulate

from metafiddler.config import MufiConfig
from metafiddler.input import Input
from metafiddler.input_events import InputEvent, EventType
from metafiddler.page import MufiPage
from metafiddler.speech import Speaker


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Starts at 1K, w/o it the pickling of the object is a no, go: maybe
# we got something else bad in here...
sys.setrecursionlimit(10000)


class Run:
    """ Main application controller """

    song_actioned = False
    queue = None
    done = False

    def provision_next_page(self, page):
        """ Callback from fork to provision the next page """
        # queue.put(page.provision())
        next_page = page.provision()
        self.queue.put(next_page, False, 2)

    def __init__(self):
        """Pre-run configurations"""

        self.config = config = MufiConfig()

        self.speaker = Speaker(config)

        self.speaker.say("Setting up current page.")

        self.current_page = MufiPage(config, config.current_page_url)

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
        events = InputEvent.events()
        for event in events:
            logging.debug("Preparing for event %s", event)
            self.speaker.prepare(event.description)

        logging.debug("Setting up current page")
        self.current_page.provision()

    def main(self):
        """Primary entrance point"""

        done = False

        while not done:
            # Download the next page while we're listening to this one so we're
            # good to go.

            # --------------------------------------------------------------------
            current_page = self.current_page

            # Set the value as
            self.config.current_page_url = current_page.audio_source_url

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

                    if event.type == EventType.PLAYLIST:
                        self.playlist(event)
                    else:
                        event.event_id()

            # This is the resolved end page which is already provisioned...
            next_page = queue.get(timeout=15)
            process.join()
            if event == InputEvent.PREVIOUS:
                current_page = current_page.links["older"]
                current_page.provision()
            else:
                current_page = next_page

    def stop(self):
        """ Stop playing the current track """
        self.current_page.song.stop()
        # Not really on this but since we're going to come back here after we
        # bail, should be A-OK.
        self.song_actioned = True
        self.done = True

    def play(self):
        """ Play (resume) the current track """
        # Maybe this should do something if its not playing?
        self.current_page.song.play()

    def next(self):
        """ Move onto the next page by closing out the current song """
        pygame.mixer.music.fadeout(100)
        self.song_actioned = True

    def previous(self):
        """ Play the previous page's track """
        pygame.mixer.music.fadeout(100)
        self.song_actioned = True

    @classmethod
    def volume_up(cls):
        """ Increase the volume """
        volume = pygame.mixer.music.get_volume()
        if volume < 1:
            pygame.mixer.music.set_volume(volume + 0.1)

    @classmethod
    def volume_down(cls):
        """ Reduce the volume """
        volume = pygame.mixer.music.get_volume()
        if volume > 0:
            pygame.mixer.music.set_volume(volume - 0.1)

    def playlist(self, playlist_id):
        """ Add the current page to the provided playlist """
        pygame.mixer.music.fadeout(100)
        if self.config.playlist_id(playlist_id):
            if not self.current_page.song.playlist_add(playlist_id):
                logging.info("Looks a bit sketchy: bailing")
                self.done = True
            # TODO: This should go into the appropriate playlist
            # subdirectory...?
        else:
            logging.warning(
                "No playlist configured for that button in this config (%s)",
                playlist_id,
            )

        self.song_actioned = True

    @classmethod
    def seek_back(cls):
        """ Go backwards in the currenly playing track """
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
        """ Go forward in the currently playing track """
        if self.current_page.song.playing():
            # Fortunately only mp3s as seek is conditional on format :O
            pygame.mixer.music.set_pos(100)

    def open_source_page(self):
        """ Open the webpage for the currently playing file """
        webbrowser.open(self.current_page.audio_source_url, new=2)
