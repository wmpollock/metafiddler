import pathlib
import yaml


# Things to save; 

# current position

current_page = ''
config_file = pathlib.Path.home() / ".metafiddlr.yaml"

def init():
    try:
        with open(config_file) as yaml_file:
            config = yaml.load(yaml_file)
        print("Loaded", config_file)
    except:
        print("No config in ", config_file)

def save():
    print("Hi, I'd be saving :[")
