"""Provides abstract interface into the wild and wolly world of TTS for our reads."""

import logging
import os
import re
import pygame.mixer
import gtts

class Speaker:
    """Class for generating, storing and recovering TTS utterances"""

    config = {}

    def __init__(self, conf):
        self.config = conf

    @classmethod
    def store(cls, utterance, file):
        """Save an utterance to a given file"""
        if not os.path.exists(file):
            tts = gtts.gTTS(utterance)
            logging.debug('Saying "%s"', utterance)
            tts.save(file)

    def prepare(self, utterance):
        """Pre-render the utterance so it is ready the moment we need it"""
        pathname = self.__utterance_path(utterance)

        if not os.path.exists(pathname):
            logging.info("Generating %s", pathname)
            self.store(utterance, pathname)

        return pathname

    def say(self, utterance):
        """Prepare and say the utterance"""
        audio = self.prepare(utterance)

        logging.debug("Playing %s", audio)
        # Does the interface need an interface, yes, probably.
        # s/b .play(file) and chump is done.
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def __utterance_path(self, utterance):
        # Too cute by far.
        # m = hashlib.md5(utterance.encode("utf-8"))
        # filename = m.hexdigest() + ".mp3"
        # Lets generate a humanish-readable
        filename = re.sub("[^a-zA-Z0-9_-]", "_", utterance)
        filename = re.sub("(^_|_$)", "", filename)
        filename = re.sub("__+", "_", filename)

        # Truncate overly long  file names, I guess potential overlap
        # but this s/b for internal commands so sort it out.
        filename = (filename[:50]) if len(filename) > 50 else filename
        filename += ".mp3"

        if not self.config.ui_reads_dir:
            logging.critical("FAILED to get dir_ui_reads for UI utterance")

        return os.path.join(self.config.ui_reads_dir, filename)
