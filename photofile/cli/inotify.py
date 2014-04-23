#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
from photofile.cli import add_common_options, check_common_options
from photofile.lib import folderwatcher


def main():
    """
    Command-line interface for using the pyinotify features of photofile.
    """
    parser = OptionParser()

    common_group = OptionGroup(parser, "Common parameters")
    common_group.add_option("-s", "--source", dest="source", help="the source folder to process")
    common_group.add_option("--dry-run", dest="dru_run", action="store_true",
                            help="Just do a test-run. No actual changes will be made")
    parser.add_option_group(common_group)

    add_common_options(parser)
    (options, args) = parser.parse_args()
    check_common_options(options, args)

    folderwatcher.run()

if __name__ == "__main__":
    main()