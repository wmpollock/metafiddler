"""Manage configuration, its persistance and the propagation of the persistence."""

import logging

import re
import os
import pathlib
from pathlib import Path
import base64
import yaml


class MufiConfig:
    """Holds file and some state information"""

    config_file = str(pathlib.Path.home() / ".metafiddler.yaml")

    # All the below values are overridable in the config
    state_file = str(pathlib.Path.home() / ".metafiddler.current")
    app_root_dir = os.path.join(str(Path.home()), "Music", "MetaFilter")
    song_save_dir = os.path.join(app_root_dir, "Songs")
    # These will have the same filename as the songs they are for
    title_reads_dir = os.path.join(app_root_dir, "Title-Reads")
    ui_reads_dir = os.path.join(app_root_dir, "User-Interface")
    _current_page = "https://music.metafilter.com/8" # earliest playable track
    
    # These are derived from ENV{MEFI_LOGIN} & ENV{MEFI_PASSWORD}, both
    # of which are bin64'd for a modicum of privacy :/
    mefi_login = ""
    mefi_password = ""

    playlists = []

    def __init__(self):
        self.mefi_login = self._de64("MEFI_LOGIN")
        self.mefi_password = self._de64("MEFI_PASSWORD")

        self._read_configfile()
        self._read_statefile()

    def _de64(self, env_name):
        env_val = os.getenv(env_name)
        if env_val:
            return base64.decodebytes(env_val.encode('utf-8')).decode('utf-8')
        else:
            logging.info("No %s value -- won't be able to playlist/favorite", env_name)
        return

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
    def current_page(self):
        """Return the value for the current page"""
        return self._current_page

    @current_page.setter
    def current_page(self, url):
        """Set the value for the current page"""
        self._current_page = url

        # Storing state file!
        with open(self.state_file, mode="w") as file:
            file.write(url)

        logging.debug("Updated state file")

    def playlist_by_label(self, playlist_label):
        """Return the playlist configuration"""
        if playlist_label in self.playlists:
            return self.playlists[playlist_label]

    def playlist_title(self, playlist_label):
        """Return the playlist title"""
        playlist = self.playlist_by_label(playlist)
        if playlist and "list_title" in playlist_label:
            return playlist["list_title"]
        else:
            return ""

    def playlist_id(self, playlist_label):
        """Return the playlist's ID"""
        playlist = self.playlist_by_label(playlist_label)

        if playlist and "list_id" in playlist:
            return playlist["list_id"]
