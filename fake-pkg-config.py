#!/usr/bin/env python3

import sys
import logging
import argparse
from pathlib import Path

# Get the absolute path of the directory containing the script
script_file = Path(__file__).absolute()
prefix_dir = script_file.parent.joinpath("build_install").resolve()

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

"""
% pkg-config --cflags ogg
-I/opt/homebrew/Cellar/libogg/1.3.5/include
% pkg-config --libs ogg
-L/opt/homebrew/Cellar/libogg/1.3.5/lib -logg
"""
packages = {
    "libtraceevent": {
        "version": "1.7.2",
        "cflags": f"-I{prefix_dir.joinpath('include/traceevent')}",
        "libs": f"-L{prefix_dir.joinpath('lib')} -ltraceevent",
    },
    "libtracefs": {
        "version": "1.6.4",
        "cflags": f"-I{prefix_dir.joinpath('include/tracefs')}",
        "libs": f"-L{prefix_dir.joinpath('lib')} -ltracefs",
    },
    "libzstd": {
        "version": "1.5.5",
        "cflags": f"-I{prefix_dir.joinpath('include')}",
        "libs": f"-L{prefix_dir.joinpath('lib')} -lzstd",
    },
    "pkg-config": {
        "variables": {
            "pc_path": f"lib/pkgconfig",
        },
    }
}

def main():
    logger.debug(" ".join(sys.argv))
    parser = argparse.ArgumentParser(description="Fuck linux build systems, they are stupid")
    parser.add_argument("--atleast-version", type=str, help="Minimum version number allowed")
    parser.add_argument("--variable", type=str, help="Minimum version number allowed")
    parser.add_argument("--cflags", action="store_true")
    parser.add_argument("--libs", action="store_true")
    parser.add_argument("package", type=str, help="Package name")
    args = parser.parse_args()
    package = packages.get(args.package, None)
    if package is None:
        logger.error(f"Unknown package: {args.package}")
        sys.exit(1)
    if args.variable:
        value = package.get("variables", {}).get(args.variable)
        if value is None:
            logger.error(f"Unknown variable {args.name}:{args.variable}")
        logger.debug(f"result: {value}")
        print(value)
        sys.exit(0)
    result = ""
    if args.cflags:
        if result:
            result += " "
        result += package["cflags"]
    if args.libs:
        if result:
            result += " "
        result += package["libs"]
    if result:
        logger.info(f"result: {result}")
        print(result)
    sys.exit(0)

if __name__ == "__main__":
    main()
