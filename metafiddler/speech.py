"""Provides abstract interface into the wild and wolly world of TTS for our reads."""
# TTS class

import hashlib
import logging
import os
import pygame.mixer
import gtts

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)


class Speaker:
    """Class for generating, storing and recovering TTS utterances"""

    config = {}

    def __init__(self, conf):
        self.config = conf

    def store(self, utterance, file):
        """Save an utterance to a given file"""
        if not os.path.exists(file):
            tts = gtts.gTTS(utterance)
            logging.debug('Saying "%s"', utterance)
            tts.save(file)

    def prepare(self, utterance):
        """Pre-render the utterance so it is ready the moment we need it"""
        pathname = self.__pathname(utterance)

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

    def __pathname(self, utterance):
        m = hashlib.md5(utterance.encode("utf-8"))

        if not self.config.ui_reads_dir:
            logging.critical("FAILED to get dir_ui_reads for UI utterance")

        return os.path.join(self.config.ui_reads_dir, m.hexdigest() + ".mp3")
