#!/usr/bin/env python

import os
import sys
import ConfigParser
from os.path import expanduser
from optparse import OptionGroup

# ------------------------------------------------------------------------
#
#                                Defaults
#
# ------------------------------------------------------------------------

default_timestamp_format = '%Y%m%d_%H%M%S'#%f
default_duplicate_filename_format = '%(filename)s~%(counter)s%(file_extension)s'
default_new_filename_format = "%(filename)s_%(timestamp)s%(file_extension)s"
default_append_timestamp = True
default_photo_extensions = ['jpg', 'nef', 'png', 'bmp', 'gif', 'cr2', 'tif', 'tiff', 'jpeg']
default_movie_extensions = ['avi', 'mov', 'mp4', 'mpg', 'mts', 'mpeg', 'mkv', '3gp', 'wmv', 'm2t']
default_ignore_files = ['thumbs.db', 'pspbrwse.jbf', 'picasa.ini', 'autorun.inf', 'hpothb07.dat']
default_ignore_folders = []
default_skip_existing = False
default_use_checksum_existence_check = False


def get_user_config_filename(folder=None):
    """
    Returns user configurations found in ~/mediaphile/mediaphile.ini or creates a configuration using defaults if it doesn't
    exist.

    :param folder: location of mediaphile.ini to use
    """
    home = os.path.abspath(folder or expanduser("~"))
    mediaphile_home = os.path.join(home, 'mediaphile')
    return os.path.join(mediaphile_home, 'mediaphile.ini')


def get_user_config(folder=None):
    """
    Returns user configurations found in ~/mediaphile/mediaphile.ini or creates a configuration using defaults if it doesn't
    exist.

    :param folder: location of mediaphile.ini to use
    """
    config_file = get_user_config_filename(folder)
    mediaphile_home = os.path.split(config_file)[0]
    config = ConfigParser.RawConfigParser()
    if not os.path.exists(mediaphile_home):
        os.makedirs(mediaphile_home)

    if not os.path.exists(config_file):
        config.add_section('options')
        config.set('options', 'timestamp format', default_timestamp_format)
        config.set('options', 'duplicate filename format', default_duplicate_filename_format)
        config.set('options', 'new filename format', default_new_filename_format)
        config.set('options', 'append timestamp', default_append_timestamp)
        config.set('options', 'photo extensions', ','.join(default_photo_extensions))
        config.set('options', 'movie extensions', ','.join(default_movie_extensions))
        config.set('options', 'ignore files', ','.join(default_ignore_files))
        config.set('options', 'ignore folders', ','.join(default_ignore_folders))
        config.set('options', 'skip existing', default_skip_existing)
        config.set('options', 'use checksum existence check', default_use_checksum_existence_check)

        with open(config_file, 'wb') as configfile:
            config.write(configfile)

    else:
        config.read(config_file)

    return config


def validate_environment():
    """
    Checks the python environment for required packages.
    """
    print("Validating running environment for mediaphile:\n")
    errors = 0
    optional = 0

    try:
        import pyexiv2

        print("PyExiv2 is installed.")
    except (ImportError):
        optional += 1
        print("PyExiv2 is missing.")

    try:
        import PIL

        print("PIL/pillow is installed.")
    except (ImportError):
        print("PIL/pillow is missing.")
        errors += 1

    try:
        import bs4

        print("BeautifulSoup/bs4 is installed.")
    except (ImportError):
        print("BeautifulSoup/bs4 is missing.")
        optional += 1

    try:
        import lxml

        print("lxml is installed.")
    except (ImportError):
        print("lxml is missing.")
        optional += 1

    try:
        import pyinotify

        print("pyinotify is installed.")
    except (ImportError):
        print("pyinotify is missing.")
        optional += 1

    print("")
    if not errors and not optional:
        print("Environment is ok.")
    else:
        print("Missing %s required and %s optional packages." % (errors, optional))

    print("")
    print("Configuration (%s) :" % get_user_config_filename())
    print("")
    config = get_user_config()
    for k, v in config.items('options'):
        print(" %s = %s" % (k.ljust(30, ' '), v))


def cb(option, opt_str, value, parser):
    """
    Callback helper function for optparser.
    """
    args = []
    for arg in parser.rargs:
        if arg[0] != "-":
            args.append(arg)
        else:
            del parser.rargs[:len(args)]
            break
    if getattr(parser.values, option.dest):
        args.extend(getattr(parser.values, option.dest))

    setattr(parser.values, option.dest, args)


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
