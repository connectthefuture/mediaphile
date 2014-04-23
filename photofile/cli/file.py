#!/usr/bin/env python

import sys
from optparse import OptionParser, OptionGroup
from photofile.cli import add_common_options, check_common_options
from photofile.lib.utils import find_duplicates


def main():
    """
    Command-line interface for using the file related features of photofile.
    """
    parser = OptionParser()

    common_group = OptionGroup(parser, "Common parameters")
    common_group.add_option("-s", "--source", dest="source", help="the source folder to process")
    common_group.add_option("-t", "--target", dest="target", help="the target folder for new files")
    common_group.add_option("--dry-run", dest="dru_run", action="store_true",
                            help="Just do a test-run. No actual changes will be made")
    parser.add_option_group(common_group)

    duplicate_group = OptionGroup(parser, "Duplicate handling")
    duplicate_group.add_option("-d", "--find_duplicates", help="locates duplicates in source folder compared to target folder",
                      dest="find_duplicates")
    duplicate_group.add_option("-x", "--delete_duplicates", action="store_true", dest="delete",
                      help="deletes any duplicate file from source folder found in both source and target folder")
    parser.add_option_group(duplicate_group)

    new_content_group = OptionGroup(parser, "Finding new files")
    new_content_group.add_option("-n", "--new_files", help="locates new files in source folder compared to target folder",
                      dest="new_files")
    parser.add_option_group(new_content_group)

    add_common_options(parser)
    (options, args) = parser.parse_args()
    check_common_options(options, args)

    if not options.source and not options.target:
        print("ERROR: You must supply both source- and target-folders.\n")
        sys.exit(1)

    elif options.find_duplicates:
        find_duplicates(options.source, options.target, delete_duplicates=options.delete, verbose=options.verbose)


if __name__ == "__main__":
    main()