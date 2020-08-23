"""Manage configuration, its persistance and the propagation of the persistence."""

import logging

import os
import pathlib
from pathlib import Path

import base64
import yaml
import requests

from metafiddler.mechanize import Browser

class MufiConfig:
    """Holds file and some state information"""

    # We need to bind the property set to save state
    _current_page = "https://music.metafilter.com/8" # earliest playable track
    app_root_dir = os.path.join(str(Path.home()), "Music", "MetaFilter")
    config_file = str(pathlib.Path.home() / ".metafiddler.yaml")
    # Remote URLs for storage -- almost went SCP but this integrates with my questionable
    # online tool O_o -- Needs more auth :]
    current_page_get_url = ""
    current_page_post_url = ""
    # All the below values are overridable in the config
    jar_file = str(pathlib.Path.home() / ".metafiddler.jar")
    state_file = str(pathlib.Path.home() / ".metafiddler.current")
    song_save_dir = os.path.join(app_root_dir, "Songs")
    # These will have the same filename as the songs they are for
    title_reads_dir = os.path.join(app_root_dir, "Title-Reads")
    ui_reads_dir = os.path.join(app_root_dir, "User-Interface")

    # These are derived from ENV{MEFI_LOGIN} & ENV{MEFI_PASSWORD}, both
    # of which are bin64'd for a modicum of privacy :/
    mefi_login = ""
    mefi_password = ""

    playlists = []

    def __init__(self):
        self.mefi_login = self._de64("MEFI_LOGIN")
        self.mefi_password = self._de64("MEFI_PASSWORD")

        # Because this is going to hit the login and needs to maintain
        # its state after so doing we're going to persist this as much as possible
        # ... This should really go into a metaclass that's used as the
        # base instead of config but its getting kinda late meyabe
        self.browser = Browser(self)

        self._read_configfile()
        self._read_statefile()

        if self.current_page_get_url:
            logging.info("Polling remote store.")
            response = requests.get(url=self.current_page_get_url)
            if response.status_code == 200:
                logging.info("Server response '%s'", response.text)
                # Lulzy -- OG architecture was clean IDs
                self._current_page = f"https://music.metafilter.com/{response.text}"
            else:
                logging.fatal("Got unexpected error code polling remote: %s", response.status_code)

    @classmethod
    def _de64(cls, env_name):
        env_val = os.getenv(env_name)
        if env_val:
            return base64.decodebytes(env_val.encode('utf-8')).decode('utf-8')

        logging.info("No %s value -- won't be able to playlist/favorite", env_name)
        return ""

    def _read_configfile(self):
        """ Load the YAML configuration file and override any class defaults """
        try:

            with open(self.config_file) as yaml_file:
                self.__dict__.update(yaml.load(yaml_file, Loader=yaml.FullLoader))
            logging.debug("Loaded %s", self.config_file)
        except FileNotFoundError:
            logging.warning("No config file %s", self.config_file)
            # Hah, well, I guess we can start at the beginning then.

    def _read_statefile(self):
        """I feel badly about having this separate and liked it all in one file but this
        content is the sharable, not-system-dependent part so ot needs to be separate"""
        try:
            with open(self.state_file, mode="r") as file:
                self._current_page = file.read()
                logging.debug("Loaded state file %s", self.state_file)
        except FileNotFoundError:
            logging.debug("State file %s does not exist.", self.state_file)


    # One-off the actual property so we can hook into setting the current_page
    @property
    def current_page_url(self):
        """Return the value for the current page"""
        return self._current_page

    @current_page_url.setter
    def current_page_url(self, url):
        """Set the value for the current page"""
        self._current_page = url

        # Storing state file!
        with open(self.state_file, mode="w") as file:
            file.write(url)
            logging.debug("Updated state file")

        if self.current_page_post_url:
            logging.info("Updating remote store.")
            response = requests.post(url=self.current_page_post_url, data=url)
            if response.status_code == 200:
                logging.info("Success")
            else:
                logging.fatal("Unexpected server response %s", response.text)


    def playlist_by_label(self, playlist_label):
        """Return the playlist configuration"""
        if playlist_label in self.playlists:
            return self.playlists[playlist_label]
        return None

    def playlist_title(self, playlist_label):
        """Return the playlist title"""
        playlist = self.playlist_by_label(playlist_label)
        if playlist and "list_title" in playlist:
            return playlist["list_title"]

        return ""

    def playlist_id(self, playlist_label):
        """Return the playlist's ID"""
        playlist = self.playlist_by_label(playlist_label)

        if playlist and "list_id" in playlist:
            return playlist["list_id"]

        logging.warning("No playlist found matching %s", playlist_label)
        return None
       