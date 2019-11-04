import gtts
import os
import os.path
from pathlib import Path
import pygame.mixer
import urllib
import unicodedata
import string


base_outdir = os.path.join(str(Path.home()), "Music", "MetaFilter")

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

pygame.mixer.init()

class MufiSong:
    """Audio-file-centric view of a MuFi song allong with metadata."""
    # MP3-taglike data
    title = ''
    artist = ''
    audio_file_url = ''
    audio_source_url = ''
    local_path = ''
    # Location of 
    title_read_path = ''
    # 
    provisioned = 0    

    def get(self,**kwargs):
        """Retrieve the audio file if it doesn't exist locally already"""
        if not self.local_path:
            self.local_path = self.__get_outpath(**kwargs)
            # Should I think pass callback if we want it; for 'fodder we would be there's
            # enough chaos going on in 'fiddler that absolutely no. 

        if os.path.exists(self.local_path):
            print(self.local_path, "already exists")
        else:
            print("Downloading", self.local_path)
            if 'callback' in kwargs:
                urllib.request.urlretrieve(self.audio_file_url, self.local_path, kwargs.get('callback'))
            else:
                urllib.request.urlretrieve(self.audio_file_url, self.local_path)

    def get_title_read(self, **kwargs):
        """Generate a TTS read of the audo description"""
        # Man, we could get fancy, but we'll save that for ho-radio

        # Like, its tempting to make a tempfile for this buuuuut I want to be able to re-run a 
        # given page to a given stage so when I pick it up I don't need to reprovision...
        # IDK, maybe more pickling is what this all calls for....
        #tts_file = tempfile.mktemp(suffix="mp3")
        if not len(self.title_read_path):
            self.title_read_path = self.__get_outpath(subdir="Title Reads")

        if os.path.exists(self.title_read_path):
            print("Title read", self.title_read_path, "exists!")
        else:
            # Irony; we worked kind of hard to split exactly this in some instances :/
            read = self.title + " by " + self.artist
            print("Title read:", read)
            print("Generating title read", self.title_read_path)
            tts = gtts.gTTS(read)
            print("Saving read")
            tts.save(self.title_read_path)


    def __get_outpath(self,**kwargs):
        # I thought maybe MeFi would be using OGG but as of 2019
        # their submissions are still.  MP3 only ¯\_(ツ)_/¯  I mean, yeet, I guess.
        # Thought I was going to have go get all up into mimetypes.guess_extension :O
        filename = self.__clean_filename(self.artist + " - " + self.title) + ".mp3"
        outdir = ''    
        # I'm going to the content in a per-playlist folder because I keep
        # my xmas music segregated and kind of don't want to load it on the 
        # accidental.  Tempting to lump 'em all together in oen subdir tho
        if 'subdir' in kwargs:
            if len(kwargs.get('subdir')):
                outdir = os.path.join(base_outdir, self.__clean_filename(kwargs.get('subdir')))
        
        if not outdir:
            #raise SystemExit("FATAL: Need to invoke with 'subdir'" + traceback.print_tb(tb[, limit[, file]])¶)
            print(kwargs)
            raise Exception("FATAL: Need to invoke with 'subdir'")

        if not os.path.exists(outdir):
            os.mkdir(outdir)

        outpath = os.path.join(outdir, filename)
        return(outpath)
    
    def play(self):
        if self.local_path:
            pygame.mixer.music.load(self.local_path)
        else:
            raise SystemExit("Local path has not been defined -- content missing :[") 
        # yeet
        pygame.mixer.music.play(0)

    def play_title(self):
        if self.title_read_path:
            pygame.mixer.music.load(self.title_read_path)
        else:
            raise SystemExit("Local path has not been defined -- content missing :[") 
        # yeet
        print("Playing title @ ", self.title_read_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


    def playing(self):
        return pygame.mixer.music.get_busy()

    # Pull down all content, in the metafiddler context we want to keep "get" separate,
    # presumably (narf)
    def provision(self, **kwargs):
        self.get(**kwargs)
        self.get_title_read(**kwargs)
    
    def stop(self):
        pygame.mixer.music.stop()

    # From https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
    def __clean_filename(self, filename, whitelist=valid_filename_chars, replace=''):
        global valid_filename_chars
        global char_limit
        
        # replace arbitrary things with underscore (default nuffin')
        for r in replace:
            filename = filename.replace(r,'_')
        
        # keep only valid ascii chars
        cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
        
        # keep only whitelisted chars
        cleaned_filename = ''.join(c for c in cleaned_filename if c in valid_filename_chars)
        if len(cleaned_filename)>char_limit:
            print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
        return cleaned_filename[:char_limit]    