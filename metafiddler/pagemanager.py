from bs4 import BeautifulSoup
import urllib.request
import re
import metafodder

def get(url, **kwargs):
    
    with urllib.request.urlopen(url) as url:
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
        page_content['title'] = title_elm['content'] 

        # Artist
        #<span class="smallcopy">posted by <a href="http://www.metafilter.com/user/124932" target="_self">TheNegativeInfluence</a> 
       
        # I'm going to crack this egg rather than try to rely on a href regexp test which IDK seems jankier?
        #artist_elm = soup.find("span", class="smallcopy", text=re.compile(r'posted by') )
        artist_elm = soup.find("a", href=re.compile(r'www.metafilter.com/user/'))
        page_content['artist'] = artist_elm.string

        #  <link rel="canonical" href="http://music.metafilter.com/8716/Down-a-Hole" id="canonical"> 
        page_content['audio_source_url'] = soup.find("link", rel="canonical")['href']

        mp3_url_regexp = re.compile(r'//mefimusic\.s3\.amazonaws\.com/.+.mp3');

        script = soup.find("script", text=mp3_url_regexp)
        if script:
            match = mp3_url_regexp.search(script.text)
            if match:
                page_content['audio_file_url'] = match.group(0)

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
                
                page_content[link_name] = {'href': 'https://music.metafilter.com' + a['href']}
            else:
                ## Might be natural case for last/first entry?  If so, don't go there
                print("FATAL: couldn't find", link_name)
                exit()

        page_content['mp3_localfile'] = metafodder.get_outpath(page_content)
    return page_content
