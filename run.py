#!/usr/bin/env python3
"""Play through Metafilter Music one song at a time"""
#  __  __      _         __ _     _     _ _
# |  \/  | ___| |_ __ _ / _(_) __| | __| | | ___ _ __
# | |\/| |/ _ \ __/ _` | |_| |/ _` |/ _` | |/ _ \ '__|
# | |  | |  __/ || (_| |  _| | (_| | (_| | |  __/ |
# |_|  |_|\___|\__\__,_|_| |_|\__,_|\__,_|_|\___|_|
#
# ----------------------------------------------------------------------------
# Desperately cruising the desolate information superhighway for tunes, man...
# Tunes.
#
# Pollock, 2019
# ============================================================================

# Command line promises made and undelivered:
# need to pass --config_file down into metafiddler.config
from metafiddler.main import Run

if __name__ == "__main__":

    run = Run()
    run.main()
