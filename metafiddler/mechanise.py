# Once we have the cookies we could cache-in:
# https://stackoverflow.com/a/33214851/8446930

import mechanize
import os.path
import pathlib

br = mechanize.Browser()

jarfle = ''
def init():
    global jarfile
    global cj

    
    jarfile = pathlib.Path.home() / "cookies.jar"
    cj = mechanize.LWPCookieJar(jarfile)
    br.set_cookiejar(cj)

    # I guess we'll assume good until we get evidence otherwise...
    if jarfile.exists():
        cj.load()
    else:
        login()

def login():
    global br
    global cj
    user_name = input("Enter username:")
    password = input("Enter password:")

    response = br.open('https://login.metafilter.com')

    br.select_form(action='logging-in.mefi')
    
    br['user_name'] = user_name
    br['user_pass'] = password

    response = br.submit()
    print(response.read())
    cj.save()

def favorite(playlist_id, mufi_id):
    global cj
    br.open("https://music.metafilter.com/contribute/add_to_playlist.mefi?id=" + str(mufi_id))
    br.select_form(action='track-add.mefi')
    print(br.form)
    br["playlist_id"] = str(playlist_id),
    response = br.submit()
    print(response.read())
    cj.save()

if __name__ == "__main__":
    login()
    favorite(365, 5334)