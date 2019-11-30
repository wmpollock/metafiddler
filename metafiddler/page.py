from bs4 import BeautifulSoup
import logging
from metafiddler.song import MufiSong
import re
import urllib.request

# Page in RSS Looks like:
# {'artist': 'TheNegativeInfluence',
#  'audio_file_url': '//mefimusic.s3.amazonaws.com/Down%20a%20Hole.mp3',
#  'audio_source_url': 'http://music.metafilter.com/8716/Down-a-Hole',
#  'list_title': '.Evaluation Hopper',
#!!! THIS IS NOT THE SAME IN 
#  'mp3_localfile': 'C:\\Users\\Bill\\Music\\MetaFilter\\.Evaluation '
#                   'Hopper\\TheNegativeInfluence - Down a Hole.mp3',
#  'newer': {'href': 'https://music.metafilter.com/8717/It-Dont-Matter-Whos-First-In-Line'},
#  'older': {'href': 'https://music.metafilter.com/8715/Manhattan-Skyline'},
#  'title': 'Down a Hole'}

mp3_url_regexp = re.compile(r'//mefimusic\.s3\.amazonaws\.com/.+.mp3')
# no trailing slash because they're not necessary per MeFi's URL handling and s/b legit to us too.
mufi_id_regexp = re.compile(r'//music\.metafilter\.com/(\d+)')

class MufiPage:
    # MP3-taglike data
    audio_source_url = ''

    # Song entity
    song = MufiSong()
    
    # PageMetadata
    links = {}

    def __str__(self):
        return str({
            "url": self.audio_source_url,
            "song": str(self.song),
            "links": str(self.links),
        })

    def __init__(self,url):
        self.audio_source_url = url
        self.song = MufiSong()

    def get(self, **kwargs):
        global mp3_url_regexp
        if self.audio_source_url:
            #logging.debug("Getting " + self.audio_source_url)
            with urllib.request.urlopen(self.audio_source_url) as url:
                content = url.read()
                soup = BeautifulSoup(content, features="lxml")

                # Title
                # ------------------------------------------------------------
                # <meta property="og:title" content="Down a Hole">
                title_elm = soup.find("meta", property="og:title")
                self.song.title = title_elm['content'] 

                # Artist
                # ------------------------------------------------------------
                #<span class="smallcopy">posted by <a href="http://www.metafilter.com/user/124932" target="_self">TheNegativeInfluence</a> 
            
                # I'm going to crack this egg rather than try to rely on a href regexp test which IDK seems jankier?
                #artist_elm = soup.find("span", class="smallcopy", text=re.compile(r'posted by') )
                artist_elm = soup.find("a", href=re.compile(r'www.metafilter.com/user/'))
                self.song.artist = artist_elm.string

                # MP3 URL
                # ------------------------------------------------------------
                #  <link rel="canonical" href="http://music.metafilter.com/8716/Down-a-Hole" id="canonical"> 
                self.song.audio_file_url = soup.find("link", rel="canonical")['href']
                script = soup.find("script", text=mp3_url_regexp)
                if script:
                    match = mp3_url_regexp.search(script.text)
                    if match:
                        # Browser fiddles about with native method, https is fine for us.
                        self.song.audio_file_url = 'https:' + match.group(0)

                # "Older" and "Newer" links
                # ------------------------------------------------------------
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
                        #logging.debug("Found " + link_name + ": https://music.metafilter.com" + a['href'])
                    # In fact /is/ natural case and undefined state (== n00bs) should start at the front w/no older :O
                    # else:
                    #     ## Might be natural case for last/first entry?  If so, don't go there
                    #     print("FATAL: couldn't find", link_name)
                    #     exit()
                
                # "mufi_id" - post number used for favorites, URLs
                # ------------------------------------------------------------
                m = mufi_id_regexp.search(self.audio_source_url)
                if m:
                    self.song.mufi_id = m.group(1)
                else:
                 #   logging.critical("FATAL coudln't find mufi_id in " + self.audio_source_url)
                    exit()

        else:
            logging.critical("FATAL: no audio source url provided to metafiddler.page")
            exit()

    def provision(self, **kwargs):
        kwargs['subdir'] = "MetaFiddler"
        self.get(**kwargs)
        self.song.provision(**kwargs)
        return self