"""Backend interaction with the web pages:  forms submittal, etc."""
# Once we have the cookiewe could cache-in:
# https://stackoverflow.com/a/33214851/8446930
import logging
import pathlib

import mechanize

OK = 200

JARFILE = pathlib.Path.home() / ".metafiddler.cookiejar"

class Browser:
    """ Handle macro interactions w/MeFi """
    logged_in = False
    browser = {}
    # Pylint can't read the 1001 instances of browser
    # pylint: disable=no-member
    def __init__(self, config):
        """Set up JARFILE and other housekeeping"""
        self.cookiejar = mechanize.LWPCookieJar()
        browser = self.browser = mechanize.Browser()
        browser.set_cookiejar(self.cookiejar)
        self.config = config

        # I guess we'll assume good until we get evidence otherwise...
        if JARFILE.exists():
            logging.debug("Loading jarfile: %s", str(JARFILE))
            self.cookiejar.load(JARFILE)
            browser.set_cookiejar(self.cookiejar)
        else:
            self.login()

    def login(self):
        """Log into MeFi"""
        if not self.config.mefi_login:
            logging.warning("Cannot perform login as there are no credentials defined.")
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

                self.cookiejar.save(JARFILE)
                self.logged_in = True
            else:
                logging.warning("Unexpected reponse code from logging in %d", response.code)

        return self.logged_in


    def playlist_add(self, playlist_id, mufi_id):
        """Add an entry to the specified playlist"""
        if not playlist_id:
            logging.fatal("Called without a playlist_id")

        if not mufi_id:
            logging.fatal("Called without a mufi_id")

        self.login()

        # try:
        response = self.browser.open(  # pylint: disable=assignment-from-none
            "https://music.metafilter.com/contribute/add_to_playlist.mefi?id="
            + str(mufi_id)
        )
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
        if response.code == OK:
            logging.info("Added sweet, sib! s( ^ ‿ ^)-b")
        else:
            logging.warning("This did not go well, we recieved response %d", response.code)

        self.cookiejar.save(JARFILE)
        return True
