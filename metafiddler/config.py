import re
import os
import pathlib
import yaml
import logging
from pathlib import Path

class MufiConfig:
    config_file = str(pathlib.Path.home() / ".metafiddler.yaml")
    
    # Define some base configurations.
    vals = {
        "metafiddler_root": os.path.join(str(Path.home()), "Music", "MetaFilter"),
        "subdir_song_save": "Songs",
        # These will have the same filename as the songs they are for
        "subdir_title_reads": "Title-Reads",
        "subdir_ui_reads": "User-Interface",
    }

    def __init__(self, **kwargs):

        try:
            # I mean, we'd need to hook it...
            if 'config_file' in kwargs:
                self.vals_file = kwargs['config_file']

            with open(self.vals_file) as yaml_file:
                self.vals.update(yaml.load(yaml_file, Loader=yaml.FullLoader))
            logging.debug("Loaded " + self.vals_file)
        except FileNotFoundError:
            logging.warning("No config file " + self.vals_file)
            # Hah, well, I guess we can start at the beginning then.
            self.current_page = "https://music.metafilter.com/8"

        # We're going to wash some values across so we're not using/
        # forcing a subdir configuration: one could configure all the paths
        # to something else outside the subdirs but this is how I'd like to
        # work with them as a configurable.
        for subdir in filter(lambda x: re.search('subdir_', x)):
            dir_opt_name = re.sub("^subdir", "dir", subdir)
            if not dir_opt_name in vals:
                vals[dir_opt_name] = os.path.join(vals['metafiddler_root'], vals[subdir])







    def get(self, value):
        if value in self.vals:
            return(self.vals[value])
        else:   
            logging.warning("No configuration vaiable named " + value)
            return()

    # Store our current URL info
    @property
    def current_page(self):
        return self.vals['current_page']

    @current_page.setter
    def current_page(self,url):
        self.vals['current_page'] = url

    @property
    def song_save_dir(self):
        return self.vals['song_save_dir']


    def playlist_config(self, playlist):
        if 'playlists' in self.vals:
            if playlist in self.vals:
                return self.vals['playlists'][playlist]

    def playlist_title(self, playlist):
        playlist=self.playlist_config(playlist)
        if playlist and 'list_title' in playlist:
            return playlist['list_title']
        else:
            return ""
            
    def playlist_id(self, playlist): 
        playlist=self.playlist_config(playlist)
        if playlist and 'list_title' in playlist:
            return playlist['list_id']
         
    def save(self):
        with open(self.vals_file, 'w') as yaml_file:
            yaml.dump(self.vals, yaml_file)
        logging.debug("Wrote state file")
    
    