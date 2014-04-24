#!/usr/bin/env python

import os
import sys
import ConfigParser
from os.path import expanduser
from optparse import OptionGroup


def get_user_config():
    """
    Returns user configurations found in ~/mediaphile/conf.ini
    """
    home = expanduser("~")
    mediaphile_home = os.path.join(home, 'mediaphile')
    config_file = os.path.join(mediaphile_home, 'conf.ini')
    config = ConfigParser.RawConfigParser()
    if not os.path.exists(mediaphile_home):
        os.makedirs(mediaphile_home)

    if not os.path.exists(config_file):
        config.add_section('options')
        config.set('options', 'timestamp format', '%Y%m%d_%H%M%S%f')
        config.set('options', 'duplicate filename_format', '%(filename)s~%(counter)s%(file_extension)s')
        config.set('options', 'new filename format', "%(filename)s_%(timestamp)s%(file_extension)s")
        config.set('options', 'append timestamp', 'true')
        config.set('options', 'photo extensions', 'jpg,nef,png,bmp,gif,cr2,tif,tiff,jpeg')
        config.set('options', 'movie extensions', 'avi,mov,mp4,mpg,mts,mpeg,mkv,3gp,wmv,m2t')
        config.set('options', 'ignore files', 'thumbs.db,pspbrwse.jbf,picasa.ini,autorun.inf,hpothb07.dat')
        config.set('options', 'ignore folders', '')

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
