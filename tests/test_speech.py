from metafiddler.speech import Speaker
from metafiddler.config import MufiConfig

if __name__ == "__main__":
    config = MufiConfig()
    pygame.mixer.init()

    s = Speaker(config)
    s.say("Audio test complete.")
