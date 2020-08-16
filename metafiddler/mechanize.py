"""Backend interaction with the web pages:  forms submittal, etc."""
# Once we have the cookiewe could cache-in:
# https://stackoverflow.com/a/33214851/8446930
import logging
import pathlib

import mechanize


jarfile = pathlib.Path.home() / ".metafiddler.cookiejar"

class Browser:
    """ Handle macro interactions w/MeFi """
    logged_in = False
    browser = {}
    def __init__(self, config):
        """Set up jarfile and other housekeeping"""
        self.cookiejar = mechanize.LWPCookieJar()
        browser = self.browser = mechanize.Browser()
        browser.set_cookiejar(self.cookiejar)
        self.config = config

        # I guess we'll assume good until we get evidence otherwise...
        if jarfile.exists():
            logging.debug("Loading jarfile: %s", str(jarfile))
            self.cookiejar.load(jarfile)
            browser.set_cookiejar(self.cookiejar)
        else:
            self.login()

    def login(self):
        """Log into MeFi"""
        if not self.config.mefi_login:
            logging.warning("Cannot perform login as there are no credentials defined in the environment.")
            return False

        if not self.logged_in:
            browser = self.browser
            browser.open("https://login.metafilter.com")

            browser.select_form(action="logging-in.mefi")

            browser["user_name"] = self.config.mefi_login # pylint: disable=unsupported-assignment-operation
            browser["user_pass"] = self.config.mefi_password # pylint: disable=unsupported-assignment-operation

            response = browser.submit()
            logging.debug("Response code: %s", response.code)
            if response.code == 200:
                # So at this point we should have a number of clues:
                # the response.read() text should has a li.profile .extra-label
                # that contains the user_name
                # the cookie jar will contain USER_NAME

                self.cookiejar.save(jarfile)
                self.logged_in = True
            else:
                logging.warning("The reponse code from logging in was unexpectedly %d", response.code)


    def playlist_add(self, playlist_id, mufi_id):
        """Add an entry to the specified playlist"""
        self.login()
        try:
            response = self.browser.open(
                "https://music.metafilter.com/contribute/add_to_playlist.mefi?id="
                + str(mufi_id)
            ) # pylint: disable=assignment-from-none
            print("Response code: ", response.code)

            # if browser.form == None:
            #     #logging.critical("Did not receive page with form.")
            #     print("Did not receive page with form.")
            #     exit()
            browser = {}
            browser = self.browser
            browser.select_form(action="track-add.mefi")
            browser["playlist_id"] = (str(playlist_id),) # pylint: disable=unsupported-assignment-operation
            response = browser.submit()
            print("Response code: ", response.code)
            return True
        except Exception as e:
            logging.fatal("Could not submit to playlist.  We have no reason left to live: %s", e)
            return False

        self.cookiejar.save(jarfile)
