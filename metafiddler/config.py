import pathlib
import yaml



# Things to save; 

#current position


current_page = ''
config_file = pathlib.Path.home() / "config.yaml"

def init():
    config = yaml.load(config_file)

def save():
    print("Hi, I'd be saving :[")
