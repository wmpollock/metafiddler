# TTS class
import gtts
import hashlib
import logging
import pygame.mixer
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


class Speaker:
    config = {}
    def __init__(self, conf, **kwargs):    
        self.config = conf

    def store(self, utterance, file):
        if not os.path.exists(file):
            tts = gtts.gTTS(utterance)
            logging.debug("Saying '" + utterance + "'")
            tts.save(file)
    
    def prepare(self, utterance):
        '''Pre-render the utterance so it is ready the moment we need it'''
        pathname = self.__pathname(utterance)

        if not os.path.exists(pathname):
            logging.info("Generating " + pathname)
            self.store(utterance, pathname)

        return(pathname)

    def say(self, utterance):
        audio = self.prepare(utterance)

        logging.debug("Playing " + audio)
        # Does the interface need an interface, yes, probably.
        # s/b .play(file) and chump is done.
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


    def __pathname(self, utterance):
        m = hashlib.md5(utterance.encode("utf-8"))

        if not self.config.get("dir_ui_reads"):
           logging.critical("FAILED to get dir_ui_reads for UI utterance")

        return(
            os.path.join(self.config.get("dir_ui_reads"),
            m.hexdigest() + ".mp3"))


if __name__ == "__main__":
    from config import MufiConfig
    config = MufiConfig()
    pygame.mixer.init()    

    s = Speaker(config)
    s.say("Aw ish")
    print("done")
    