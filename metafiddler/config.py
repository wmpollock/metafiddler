import pathlib
import yaml
import logging


class MufiConfig:
    config_file = str(pathlib.Path.home() / ".metafiddlr.yaml")
    config = {}

    def __init__(self, **kwargs):
        
        try:
            # I mean, we'd need to hook it...
            if 'config_file' in kwargs:
                self.config_file = kwargs['config_file']

            with open(self.config_file) as yaml_file:
                self.config = yaml.load(yaml_file, Loader=yaml.FullLoader)
            logging.debug("Loaded " + self.config_file)
        except FileNotFoundError:
            logging.warning("No config file " + self.config_file)
            # Hah, well, I guess we can start at the beginning then.
            self.current_page = "https://music.metafilter.com/8"

    @property
    def current_page(self):
        return self.config['current_page']

    @current_page.setter
    def current_page(self,url):
        self.config['current_page'] = url


    def playlist_config(self, playlist):
        if 'playlists' in self.config:
            if playlist in self.config:
                return self.config['playlists'][playlist]

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
            yaml.dump(self.config, yaml_file)
        logging.debug("Wrote state file")
