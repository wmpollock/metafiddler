"""The individual song entity and methods therefore."""
import logging
import os
import os.path
import urllib
import unicodedata
import string
import sys
import pygame.mixer

from metafiddler.speech import Speaker


VALID_FILENAME_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
CHAR_LIMIT = 255

# if __name__ == '__main__':
# Someone has to do it and we're the player so...
pygame.mixer.init()


class MufiSong:
    """Audio-file-centric view of a MuFi song allong with metadata."""

    config = {}
    # MP3-taglike data
    title = ""
    artist = ""
    audio_file_url = ""
    audio_source_url = ""
    local_path = ""
    mufi_id = 0
    # TTS object for the speaker, s/b consistent but maybe not the same
    # as UI
    speaker = {}

    # Location of mp3 for title read
    title_read_path = ""
    # Flag whether we've gotten data -- I'm sure I had a purpose...
    provisioned = 0

    def __init__(self, c):
        self.config = c
        self.speaker = Speaker(self.config)


    def __str__(self):
        return str({"title", self.title, "artist", self.artist})

    def get(self, **kwargs):
        """Retrieve the audio file if it doesn't exist locally already"""
        if not self.local_path:
            # All songs should go into the same folder unless
            # we've got a specific home for them (playlist folders: currently
            # just vestigal from metafodder)
            if "dir" not in kwargs:
                if self.config.song_save_dir:
                    kwargs["dir"] = self.config.song_save_dir
                else:
                    logging.critical("FATAL: unable no 'dir_song_save' config")
                    sys.exit(1)

            self.local_path = self.__get_outpath(**kwargs)

            # Should I think pass callback if we want it; for 'fodder we would be there's
            # enough chaos going on in 'fiddler that absolutely no.

        if os.path.exists(self.local_path):
            logging.debug("%s already exists", self.local_path)
        else:
            logging.debug("Downloading %s ", self.local_path)
            if "callback" in kwargs:
                urllib.request.urlretrieve(
                    self.audio_file_url, self.local_path, kwargs.get("callback")
                )
            else:
                urllib.request.urlretrieve(self.audio_file_url, self.local_path)

    def get_title_read(self):
        """Generate a TTS read of the audo description"""
        # Man, we could get fancy, but we'll save that for ho-radio

        # Like, its tempting to make a tempfile for this buuuuut I want to be able to re-run a
        # given page to a given stage so when I pick it up I don't need to reprovision...
        # IDK, maybe more pickling is what this all calls for....
        # tts_file = tempfile.mktemp(suffix="mp3")
        if self.title_read_path == "":
            self.title_read_path = self.__get_outpath(
                dir=self.config.title_reads_dir
            )

        if os.path.exists(self.title_read_path):
            logging.debug("Title read %s already exists.", self.title_read_path)
        else:
            # Irony; we worked kind of hard to split exactly this in some instances :/
            read = self.title + " by " + self.artist
            logging.debug("Title read: %s", read)
            logging.debug("Generating title read file %s", self.title_read_path)

            self.speaker.store(read, self.title_read_path)

    # I tried subclassing self as part of pygame.mixer.music but I'm obv. doing
    # something wrong :/
    @classmethod
    def pause(cls):

        """Suspend playing music"""
        pygame.mixer.music.pause()

    @classmethod
    def stop(cls):
        """Stop playing music: position is lost."""
        pygame.mixer.music.stop()

    def play(self):
        """Begin playing the song"""
        if self.local_path:
            logging.info("Playing song: %s", self.local_path)
            pygame.mixer.music.load(self.local_path)
        else:
            raise SystemExit("Local path has not been defined -- content missing :[")
        # yeet
        pygame.mixer.music.play(0)

    def play_title(self):
        """Play the TTS read of the title"""
        if self.title_read_path:
            pygame.mixer.music.load(self.title_read_path)
        else:
            raise SystemExit("Local path has not been defined -- content missing :[")
        # yeet
        logging.info("Playing title read: %s", self.title_read_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    @classmethod
    def playing(cls):
        """Determine whether a song is currently playing"""
        try:
            return pygame.mixer.music.get_busy()
        except KeyboardInterrupt:
            print("Ending on keyboard termination.")
            sys.exit(1)

    def playlist_add(self, playlist_id):
        """Add this song to a playlist (deleates to .mechanize)"""
        return self.config.browser.playlist_add(playlist_id, self.mufi_id)

    def provision(self, **kwargs):
        """Pull down all content, in the metafiddler context we want to keep "get" separate,
    presumably (narf)"""
        self.get(**kwargs)
        self.get_title_read(**kwargs)

    # From https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
    @classmethod
    def __clean_filename(cls, filename):
        """ replace arbitrary things with underscore (default nuffin')"""

        # keep only valid ascii chars
        cleaned_filename = (
            unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore").decode()
        )

        # keep only whitelisted chars
        cleaned_filename = "".join(
            c for c in cleaned_filename if c in VALID_FILENAME_CHARS
        )
        if len(cleaned_filename) > CHAR_LIMIT:
            logging.warning(
                "Warning, filename truncated because it was over %s. "
                "Filenames may no longer be unique",
                CHAR_LIMIT,
            )
        return cleaned_filename[:CHAR_LIMIT]

    def __get_outpath(self, **kwargs):
        """Buid the output path for this song"""
        # I thought maybe MeFi would be using OGG but as of 2019
        # their submissions are still.  MP3 only ¯\_(ツ)_/¯  I mean, yeet, I guess.
        # Thought I was going to have go get all up into mimetypes.guess_extension :O
        filename = self.__clean_filename(self.artist + " - " + self.title) + ".mp3"

        # I'm going to the content in a per-playlist folder because I keep
        # my xmas music segregated and kind of don't want to load it on the
        # accidental.  Tempting to lump 'em all together in oen subdir tho
        if "dir" not in kwargs:

            logging.critical("Yikes, outpath invoked without 'dir'")
            sys.exit(1)

        outdir = kwargs["dir"]

        # I was like, nah, but then, yeah, with this config nonsense
        if not outdir:
            raise ValueError("FATAL: Need to invoke with 'dir' defined")

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        outpath = os.path.join(outdir, filename)
        return outpath
