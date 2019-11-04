from bs4 import BeautifulSoup
import urllib.request
import re
from metafiddler.song import MufiSong


mp3_url_regexp = re.compile(r'//mefimusic\.s3\.amazonaws\.com/.+.mp3');

class MufiPage:
    # MP3-taglike data
    audio_source_url = ''

    # Song entity
    song = MufiSong()
    
    # PageMetadata
    links = {}

    def __str__(self):
        return str({
            "song": self.song,
            "links": self.links
        })

    def __init__(self,url):
        self.audio_source_url = url


    def get(self, **kwargs):
        global mp3_url_regexp
        print("Getting", self.audio_source_url)
        with urllib.request.urlopen(self.audio_source_url) as url:
            content = url.read()
            
            page_content = {'audio_source_url': url,
                            # We're going to give it this kinda janky folder name to store things
                            # While we play through them.  Also it helps the naming
                            'list_title': ".Evaluation Hopper"
                            }

            soup = BeautifulSoup(content, features="lxml")

            # Title
            # <meta property="og:title" content="Down a Hole">
            title_elm = soup.find("meta", property="og:title")
            self.song.title = title_elm['content'] 

            # Artist
            #<span class="smallcopy">posted by <a href="http://www.metafilter.com/user/124932" target="_self">TheNegativeInfluence</a> 
        
            # I'm going to crack this egg rather than try to rely on a href regexp test which IDK seems jankier?
            #artist_elm = soup.find("span", class="smallcopy", text=re.compile(r'posted by') )
            artist_elm = soup.find("a", href=re.compile(r'www.metafilter.com/user/'))
            self.song.artist = artist_elm.string

            #  <link rel="canonical" href="http://music.metafilter.com/8716/Down-a-Hole" id="canonical"> 
            self.song.audio_file_url = soup.find("link", rel="canonical")['href']

            script = soup.find("script", text=mp3_url_regexp)
            if script:
                match = mp3_url_regexp.search(script.text)
                if match:
                    # Browser fiddles about with native method, https is fine for us.
                    self.song.audio_file_url = 'https:' + match.group(0)

            links = {
                "older": {
                    "regexp": re.compile(r'Older')
                },
                "newer": {
                    "regexp": re.compile(r'Newer')
                }
            }
            for link_name, link_vals in links.items():
                # The title for this is contained in nothing partiularly semantic, just hanging:
                # out in a .comments > .whitesmallcopy containing this here a
                # <a (newer)/> TITLE_A | TITLE_B <a (older)/>
                # IDK, I don't have a strong use case (maybe)
                a = soup.find("a", text=link_vals['regexp'])
                if a:
                    # Links are not (currently) fully qualified
                    self.links[link_name] = MufiPage('https://music.metafilter.com' + a['href'])
                else:
                    ## Might be natural case for last/first entry?  If so, don't go there
                    print("FATAL: couldn't find", link_name)
                    exit()
            

    def provision(self, **kwargs):
        self.get(**kwargs)
        self.song.provision(**kwargs)
        return self