# Once we have the cookiewe could cache-in:
# https://stackoverflow.com/a/33214851/8446930
import logging
import mechanize
import os.path
import pathlib

br = mechanize.Browser()

jarfile = pathlib.Path.home() / ".metafiddler.cookiejar"

def init():
    global jarfile
    global cj

    cj = mechanize.LWPCookieJar()
    br.set_cookiejar(cj)

    # I guess we'll assume good until we get evidence otherwise...
    if jarfile.exists():
        logging.debug("Loading jarfile: " + str(jarfile))
        cj.load(jarfile)
        br.set_cookiejar(cj)
    else:
        login()

logged_in = 0
def login():
    global jarfile
    global br
    global cj
    global logged_in
    
    if not logged_in:
        user_name = input("Enter username: ")
        password = input("Enter password: ")

        br.open('https://login.metafilter.com')

        br.select_form(action='logging-in.mefi')
        
        br['user_name'] = user_name
        br['user_pass'] = password

        response = br.submit()
        print("Response code: ", response.code)
        # So at this point we should have a number of clues:
        #   the response.read() text should has a li.profile .extra-label that contains the user_name
        #   the cookie jar will contain USER_NAME
        
        cj.save(jarfile)
        logged_in = 1

def playlist_add(playlist_id, mufi_id):
    global cj
    login()
    try:
        response = br.open("https://music.metafilter.com/contribute/add_to_playlist.mefi?id=" + str(mufi_id))
        print("Response code: ", response.code)


        # if br.form == None:
        #     #logging.critical("Did not receive page with form.")
        #     print("Did not receive page with form.")
        #     exit()

        br.select_form(action='track-add.mefi')
        br["playlist_id"] = str(playlist_id),
        response = br.submit()
        print("Response code: ", response.code)
        return True
    except:
        logging.fatal("Could not submit to playlist.  We have no reason left to live.")
        return False

    #print(response.read())
    cj.save(jarfile)
