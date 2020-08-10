from metafiddler.config import MufiConfig


if __name__ == "__main__":
    logging.debug("Datatest")
    config = MufiConfig()


    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(config.vals)
    print(config.playlist_id("playlist_b"))
