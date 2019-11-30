import pathlib
import yaml

# Things to save; 
# current position

class MufiConfig:
    config_file = pathlib.Path.home() / ".metafiddlr.yaml"
    config = {}

    def __init__(self, **kwargs):
        
        try:
            # I mean, we'd need to hook it...
            if 'config_file' in kwargs:
                self.config_file = kwargs['config_file']

            with open(self.config_file) as yaml_file:
                self.config = yaml.load(yaml_file)
            print("Loaded", self.config_file)
        except FileNotFoundError:
            print("No config in ", self.config_file)
            # Hah, well, I guess we can start at the beginning then.
            self.current_page = "https://music.metafilter.com/8"

    @property
    def current_page(self):
        return self.config['current_page']

    @current_page.setter
    def current_page(self,url):
        self.config['current_page'] = url

    def playlist_title(self, playlist):
        print(self.config)
        return self.config['playlists'][playlist]['list_title']

    def playlist_id(self, playlist):
        return self.config['playlists'][playlist]['list_id']
        
    def save(self):
        with open(self.config_file, 'w') as yaml_file:
            yaml.dump(self.config, yaml_file)
        print("Wrote state file")
