#!/usr/bin/env python

import sys
import logging
from pathlib import Path

# Get the absolute path of the directory containing the script
script_file = Path(__file__)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler that logs to a file in the script directory
log_path = script_file.parent.joinpath(script_file.stem + ".log")
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def main():
    logger.debug(" ".join(sys.argv))
    sys.exit(1)

if __name__ == "__main__":
    main()
