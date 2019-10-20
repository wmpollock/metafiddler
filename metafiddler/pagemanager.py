from bs4 import BeautifulSoup
import urllib.request
import re

def get(url):
    
    with urllib.request.urlopen(url) as url:
        content = url.read()
        
        page_content = {}

        soup = BeautifulSoup(content, features="lxml")

        mp3UrlRegexp = re.compile(r'//mefimusic\.s3\.amazonaws\.com/.+.mp3');

        script = soup.find("script", text=mp3UrlRegexp)
        if script:
            match = mp3UrlRegexp.search(script.text)
            if match:
                page_content['mp3_url'] = match.group(0)

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

        
    return page_content
