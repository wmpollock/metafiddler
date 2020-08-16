"""Backend interaction with the web pages:  forms submittal, etc."""
# Once we have the cookiewe could cache-in:
# https://stackoverflow.com/a/33214851/8446930
import logging
import pathlib

import mechanize



jarfile = pathlib.Path.home() / ".metafiddler.cookiejar"

class Browser:
    logged_in = False

    def __init__(self, config ):
        """Set up jarfile and other housekeeping"""
         self.cj = mechanize.LWPCookieJar()
        br = self.br = mechanize.Browser()
        br.set_cookiejar(self.cj)
        self.config = config

        # I guess we'll assume good until we get evidence otherwise...
        if jarfile.exists():
            logging.debug("Loading jarfile: %s", str(jarfile))
            cj.load(jarfile)
            br.set_cookiejar(self.cj)
        else:
            self.login()

    def login(self):
        """Log into MeFi"""
        if not self.config.mefi_login:
            logging.warning("Cannot perform login as there are no credentials defined in the environment.")
            return False

        if self.logged_in == False:
            br = self.br
            br.open("https://login.metafilter.com")

            br.select_form(action="logging-in.mefi")

            br["user_name"] = self.config.mefi_login
            br["user_pass"] = self.config.mefi_password

            response = br.submit()
            logging.debug("Response code: %s", response.code)
            # So at this point we should have a number of clues:
            # the response.read() text should has a li.profile .extra-label
            # that contains the user_name
            # the cookie jar will contain USER_NAME

            self.cj.save(jarfile)
            self.logged_in = True


    def playlist_add(self, playlist_id, mufi_id):
        """Add an entry to the specified playlist"""
        login()
        try:
            response = self.br.open(
                "https://music.metafilter.com/contribute/add_to_playlist.mefi?id="
                + str(mufi_id)
            )
            print("Response code: ", response.code)

            # if br.form == None:
            #     #logging.critical("Did not receive page with form.")
            #     print("Did not receive page with form.")
            #     exit()

            br.select_form(action="track-add.mefi")
            br["playlist_id"] = (str(playlist_id),)
            response = br.submit()
            print("Response code: ", response.code)
            return True
        except:
            logging.fatal("Could not submit to playlist.  We have no reason left to live.")
            return False

        # print(response.read())
        cj.save(jarfile)
