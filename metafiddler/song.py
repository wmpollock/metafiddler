import os
import os.path
import urllib
import unicodedata
import string


valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


class MufiSong:
    # MP3-taglike data
    title = ''
    artist = ''
    audio_file_url = ''
    audio_source_url = ''
    local_path = ''

    def get(self,**kwargs):
        if not self.local_path:
            self.local_path = self.get_outpath(**kwargs)
            # Should I think pass callback if we want it; for 'fodder we would be there's
            # enough chaos going on in 'fiddler that absolutely no. 

        if os.path.exists(outdir):
            print(outdir, "already exists")
        else:
            print("Downloading", outdir)
            if 'callback' in kwargs:
                urllib.request.urlretrieve(self.audio_file_url, file_info['path'], kwargs.get('callback'))
            else:
                urllib.request.urlretrieve(self.audio_file_url, file_info['path'])
           
    def get_outpath(self,**kwargs):
        # I thought maybe MeFi would be using OGG but as of 2019
        # their submissions are still.  MP3 only ¯\_(ツ)_/¯  I mean, yeet, I guess.
        # Thought I was going to have go get all up into mimetypes.guess_extension :O
        filename = self._clean_filename(self.artist + " - " + self.title) + ".mp3"
        outdir = ''    
        # I'm going to the content in a per-playlist folder because I keep
        # my xmas music segregated and kind of don't want to load it on the 
        # accidental.  Tempting to lump 'em all together in oen subdir tho
        if 'subdir' in kwargs:
            if len(kwargs.get('subdir')):
                outdir = os.path.join(base_outdir, clean_filename.convert(kwargs.get('subdir')))
        
        if not outdir:
            #raise SystemExit("FATAL: Need to invoke with 'subdir'" + traceback.print_tb(tb[, limit[, file]])¶)
            raise Exception("FATAL: Need to invoke with 'subdir'")

        if not os.path.exists(outdir):
            os.mkdir(outdir)

        outpath = os.path.join(outdir, filename)
        return(outpath)
    
    def play(self):
    # mixer.init()
        if self.local_path:
            pygame.mixer.music.load(self.local_path)
        else:
            raise SystemExit("Local path has not been defined -- content missing :[") 
        # mixer.music.play(0)


    # From https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
    def _clean_filename(self, filename, whitelist=valid_filename_chars, replace=''):
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