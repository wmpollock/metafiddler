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
        # "metafiddler_root": os.path.join(str(Path.home()), "Music", "MetaFilter"),
        # "subdir_song_save": "Songs",
        # # These will have the same filename as the songs they are for
        # "subdir_title_reads": "Title-Reads",
        # "subdir_ui_reads": "User-Interface",
    }

    def __init__(self, **kwargs):

        self.vals = {
            "metafiddler_root": os.path.join(str(Path.home()), "Music", "MetaFilter"),
            "subdir_song_save": "Songs",
            # These will have the same filename as the songs they are for
            "subdir_title_reads": "Title-Reads",
            "subdir_ui_reads": "User-Interface",
        }
        try:
            # I mean, we'd need to hook it...
            if 'config_file' in kwargs:
                self.config_file = kwargs['config_file']

            with open(self.config_file) as yaml_file:
                self.vals.update(yaml.load(yaml_file, Loader=yaml.FullLoader))
            logging.debug("Loaded " + self.config_file)
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.vals)
        except FileNotFoundError:
            logging.warning("No config file " + self.config_file)
            # Hah, well, I guess we can start at the beginning then.
            self.current_page = "https://music.metafilter.com/8"

        # We're going to wash some values across so we're not using/
        # forcing a subdir configuration: one could configure all the paths
        # to something else outside the subdirs but this is how I'd like to
        # work with them as a configurable.
        # s/subdir_foo/di_roo
        # Have to extract since filter will get fussy about changing dict mideway
        subdirs = list(filter(lambda x: re.search('subdir_', x), self.vals.keys()))
        if not self.vals['metafiddler_root']:
            logging.critical("Metafiddler root not set")
            return(0)
        for subdir in subdirs:
            dir_opt_name = re.sub("^subdir", "dir", subdir)
            if not dir_opt_name in self.vals:
                self.vals[dir_opt_name] = os.path.join(self.vals['metafiddler_root'], self.vals[subdir])
                logging.debug("Set", dir_opt_name, self.vals[dir_opt_name])
                if not os.path.exists(self.vals[dir_opt_name]):
                    os.makedirs(self.vals[dir_opt_name])






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
        with open(self.config_file, 'w') as yaml_file:
            yaml.dump(self.vals, yaml_file)

        logging.debug("Wrote state file")
    
    