#!/usr/bin/env python
import sys
from optparse import OptionParser, OptionGroup
from mediaphile.lib.movies import relocate_movies
from mediaphile.cli import add_common_options, check_common_options


def main():
    """
    Command-line interface for using the movie related features of photofile.
    """
    parser = OptionParser()

    common_group = OptionGroup(parser, "Relocates movies by creation date into a date-based hierarchy")
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
        sys.exit(1)

    elif options.relocate_movies:
        relocate_movies(options.source, options.target)


if __name__ == "__main__":
    main()