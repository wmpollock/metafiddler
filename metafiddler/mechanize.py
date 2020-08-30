"""Backend interaction with the web pages:  forms submittal, etc."""
# Once we have the cookiewe could cache-in:
# https://stackoverflow.com/a/33214851/8446930
import logging
import pathlib
import sys

import mechanize


OK = 200

JARFILE = pathlib.Path.home() / ".metafiddler.cookiejar"

class Browser(mechanize.Browser):
    """ Handle macro interactions w/MeFi """
    logged_in = False
    # Pylint can't read the 1001 instances of browser
    # pylint: disable=no-member
    def __init__(self, config):
        """Set up JARFILE and other housekeeping"""
        self.config = config

        # I guess we'll assume good until we get evidence otherwise...
        if JARFILE.exists():
            logging.debug("Loading jarfile: %s", str(JARFILE))
            self.cookiejar = mechanize.LWPCookieJar(JARfiLE)
        else:
            self.login()

    def login(self):
        """Log into MeFi"""
        if not self.config.mefi_login:
            logging.warning("Cannot perform login as there are no credentials defined.")
            return False

        if not self.logged_in:
            self.open("https://login.metafilter.com")

            self.select_form(action="logging-in.mefi")

            self["user_name"] = self.config.mefi_login # pylint: disable=unsupported-assignment-operation
            self["user_pass"] = self.config.mefi_password # pylint: disable=unsupported-assignment-operation

            response = self.submit()
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
            logging.critical("Called without a playlist_id")
            sys.exit(1)

        if not mufi_id:
            logging.critical("Called without a mufi_id")
            sys.exit(1)

        self.login()

        # try:
        response = self.open(  # pylint: disable=assignment-from-none
            "https://music.metafilter.com/contribute/add_to_playlist.mefi?id="
            + str(mufi_id)
        )
        print("Response code: ", response.code)

        self.select_form(action="track-add.mefi")


        self["playlist_id"] = (str(playlist_id),) # pylint: disable=unsupported-assignment-operation
        response = self.submit()
        if response.code == OK:
            logging.info("Added sweet, sib! s( ^ ‿ ^)-b")
        else:
            logging.warning("This did not go well, we recieved response %d", response.code)

        self.cookiejar.save(JARFILE)
        return True
