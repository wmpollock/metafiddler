"""Manage configuration, its persistance and the propagation of the persistence."""

import logging

import re
import os
import pathlib
from pathlib import Path

import yaml


class MufiConfig:
    """Holds file and some state information"""
    config_file = str(pathlib.Path.home() / ".metafiddler.yaml")
    state_file = str(pathlib.Path.home() / ".metafiddler.current")

    # Define some base configurations.
    vals = {}

    def __init__(self):

        self.vals = {
            "metafiddler_root": os.path.join(str(Path.home()), "Music", "MetaFilter"),
            "subdir_song_save": "Songs",
            # These will have the same filename as the songs they are for
            "subdir_title_reads": "Title-Reads",
            "subdir_ui_reads": "User-Interface",
            "current_page": "https://music.metafilter.com/8"
        }
        self._read_configfile()
        self._read_statefile()


    def _read_configfile(self):

        try:

            with open(self.config_file) as yaml_file:
                self.vals.update(yaml.load(yaml_file, Loader=yaml.FullLoader))
            logging.debug("Loaded %s", self.config_file)
        except FileNotFoundError:
            logging.warning("No config file %s", self.config_file)
            # Hah, well, I guess we can start at the beginning then.


        # We're going to wash some values across so we're not using/
        # forcing a subdir configuration: one could configure all the paths
        # to something else outside the subdirs but this is how I'd like to
        # work with them as a configurable.
        # s/subdir_foo/di_roo
        # Have to extract since filter will get fussy about changing dict mideway
        if not self.vals['metafiddler_root']:
            logging.critical("Metafiddler root not set")
            raise ValueError("Metafiddler root not set")

        # Generate fuller subdirectory names for quicker use
        subdirs = list(filter(lambda x: re.search('subdir_', x), self.vals.keys()))
        for subdir in subdirs:
            dir_opt_name = re.sub("^subdir", "dir", subdir)
            if not dir_opt_name in self.vals:
                self.vals[dir_opt_name] = os.path.join(
                    self.vals['metafiddler_root'],
                    self.vals[subdir]
                )
                logging.debug("Set %s to %s", dir_opt_name, self.vals[dir_opt_name])
                if not os.path.exists(self.vals[dir_opt_name]):
                    os.makedirs(self.vals[dir_opt_name])


    def _read_statefile(self):
        """I feel badly about having this separate and liked it all in one file but this
        content is the sharable, not-system-dependent part so ot needs to be separate"""
        try:
            with open(self.state_file, mode='r') as file:
                self.vals['current_page'] = file.read()
                logging.debug("Loaded state file %s", self.state_file)
        except FileNotFoundError:
            logging.debug("State file %s does not exist.", self.state_file)


    def get(self, value):
        # TODO -- feels janky
        """Retrieve a specific value"""
        if value in self.vals:
            return self.vals[value]
        else:
            logging.warning("No configuration vaiable named %s", value)
            return

    # I think this access method in the grand scheme didn't scale very well
    # and should be burned for crap.

    # Store our current URL info
    @property
    def current_page(self):
        """Return the value for the current page"""
        return self.vals['current_page']

    @current_page.setter
    def current_page(self, url):
        """Set the value for the current page"""
        self.vals['current_page'] = url

        # Storing state file!
        with open(self.state_file, mode='w') as file:
            file.write(url)

        logging.debug("Wrote state file")


    @property
    def song_save_dir(self):
        """Return the directory for saving songs"""
        return self.vals['song_save_dir']

    # TODO - this should be a Playlist object
    def playlist_config(self, playlist):
        """Return the playlist configuration"""
        if 'playlists' in self.vals:
            if playlist in self.vals['playlists']:
                return self.vals['playlists'][playlist]

    def playlist_title(self, playlist):
        """Return the playlist title"""
        playlist = self.playlist_config(playlist)
        if playlist and 'list_title' in playlist:
            return playlist['list_title']
        else:
            return ""

    def playlist_id(self, playlist):
        """Return the playlist's ID"""
        playlist = self.playlist_config(playlist)

        if playlist and 'list_title' in playlist:
            return playlist['list_id']

