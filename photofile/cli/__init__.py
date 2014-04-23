#!/usr/bin/env python

import os
import sys
import ConfigParser
from os.path import expanduser
from optparse import OptionParser, OptionGroup
from photofile.utils import relocate_photos


def get_user_config():
    """
    Returns user configurations found in ~/photofile/conf.ini
    """
    home = expanduser("~")
    photofile_home = os.path.join(home, 'photofile')
    config_file = os.path.join(photofile_home, 'conf.ini')
    config = ConfigParser.RawConfigParser()
    if not os.path.exists(photofile_home):
        os.makedirs(photofile_home)

    if not os.path.exists(config_file):
        config.add_section('options')
        config.set('options', 'timestamp_format', '%Y%m%d_%H%M%S%f')
        config.set('options', 'duplicate_filename_format', '%(filename)s~%(counter)s%(file_extension)s')
        config.set('options', 'new_filename_format', "%(filename)s_%(timestamp)s%(file_extension)s")

        with open(config_file, 'wb') as configfile:
            config.write(configfile)

    else:
        config.read(config_file)

    return config


def validate_environment():
    """
    Checks the python environment for required packages.
    """
    print("Validating running environment for photofile:\n")
    errors = 0
    try:
        import pyexiv2
        print("PyExiv2 is installed.")
    except (ImportError):
        errors += 1
        print("PyExiv2 is missing.")

    try:
        import PIL
        print("PIL/pillow is installed.")
    except (ImportError):
        print("PIL/pillow is missing.")
        errors += 1

    if not errors:
        print("Environment is ok.")
    else:
        print("Missing %s required packages." % errors)


def cb(option, opt_str, value, parser):
    """
    Callback helper function for optparser.
    """
    args=[]
    for arg in parser.rargs:
            if arg[0] != "-":
                    args.append(arg)
            else:
                    del parser.rargs[:len(args)]
                    break
    if getattr(parser.values, option.dest):
            args.extend(getattr(parser.values, option.dest))

    setattr(parser.values, option.dest, args)


def print_help(parser):
    """
    Prints help for the command-line interface for photofile along with some examples of use.
    :param parser: an optparser instance.
    """
    parser.print_help()
    print("")
    print("Examples of use:")
    print("")
    print("To relocate photos and generate a date-based hierarchy from EXIF-date:")
    print("$ photofile -p -s /home/thomas/Pictures/New -t /home/thomas/Pictures/Sorted")


def add_common_options(parser):
    debug_group = OptionGroup(parser, "Debug options")
    debug_group.add_option("-c", "--validate_environment", dest="validate_environment", action="store_true",
                           help="Validates the python environment and checks for required packages")
    debug_group.add_option("-v", "--verbose", action="store_true", dest="verbose", help="verbose logging")
    parser.add_option_group(debug_group)


def check_common_options(options, args):

    if options.validate_environment:
        validate_environment()
        sys.exit(0)

    if hasattr(options, 'source') and options.source:
        options.source = os.path.abspath(options.source)

    if hasattr(options, 'target') and options.target:
        options.target = os.path.abspath(options.target)


def main():
    """
    Command-line interface for using photofile.
    """
    config = get_user_config()
    print(config)
    print(config.get('options', 'timestamp_format'))

    parser = OptionParser()

    common_group = OptionGroup(parser, "Common parameters")
    common_group.add_option("-s", "--source", dest="source", help="the source folder to process")
    common_group.add_option("-t", "--target", dest="target", help="the target folder for new files")
    common_group.add_option("--dry-run", dest="dru_run", action="store_true",
                            help="Just do a test-run. No actual changes will be made")
    parser.add_option_group(common_group)

    photo_group = OptionGroup(parser, "Photo organization")
    photo_group.add_option("-p", "--relocate_photos",
                      help="relocates photos and images by EXIF/creation date into a date-based hierarchy",
                      dest="relocate_photos", action="store_true")
    photo_group.add_option("-i", "--search_sidecar", dest="sidecar_keywords", action="callback", callback=cb,
                      help="Searches any sidecar/XMP-files found in target for tags with a specific content")
    parser.add_option_group(photo_group)

    add_common_options(parser)

    (options, args) = parser.parse_args()

    check_common_options(options, args)

    if not options.source and not options.target:
        print("ERROR: You must supply both source- and target-folders.\n")
        print_help(parser)
        sys.exit(1)

    elif options.relocate_photos:
        relocate_photos(options.source, options.target)



if __name__ == "__main__":
    main()