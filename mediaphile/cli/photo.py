#!/usr/bin/env python

import sys
from optparse import OptionParser, OptionGroup
from mediaphile.lib.utils import relocate_photos
from mediaphile.cli import add_common_options, check_common_options


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


def main():
    """
    Command-line interface for using photo and image related functions of photofile.
    """
    parser = OptionParser()

    common_group = OptionGroup(parser, "Relocates photos and images by EXIF/creation date into a date-based hierarchy")
    common_group.add_option("-s", "--source", dest="source", help="the source folder to process")
    common_group.add_option("-t", "--target", dest="target", help="the target folder for new files")
    common_group.add_option("--dry-run", dest="dru_run", action="store_true",
                            help="Just do a test-run. No actual changes will be made")
    parser.add_option_group(common_group)

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