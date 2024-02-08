"""
This config file holds all the directory location for the csv, arb files for now.
We can add other configurable params on it as a regular python variable.
"""
from pathlib import PurePath

# Base directory for this module (arb_generator)
BASE_DIR = PurePath(__file__).parent

# Csv file location
CSV_FILE = BASE_DIR.joinpath("csv", "lang.csv")

# Arb files directory location
ARB_DIR = BASE_DIR.joinpath('arb')

# Arb file prefix name
ARB_FILE_PREFIX = "intl_"

# Arb file extension
ARB_FILE_EXT = ".arb"
