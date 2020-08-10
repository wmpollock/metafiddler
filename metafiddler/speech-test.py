import metafiddler.speech
from config import MufiConfig

if __name__ == "__main__":
    config = MufiConfig()
    pygame.mixer.init()    

    s = Speaker(config)
    s.say("Aw ish")
    print("done")
