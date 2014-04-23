#!/usr/bin/env python

import sys
from optparse import OptionParser, OptionGroup
from photofile.cli import add_common_options, check_common_options


def main():
    """
    Command-line interface for using the thumbnail features of photofile.
    """
    parser = OptionParser()

    common_group = OptionGroup(parser, "Common parameters")
    common_group.add_option("-s", "--source", dest="source", help="the source folder to process")
    common_group.add_option("-t", "--target", dest="target", help="the target folder for new files")
    common_group.add_option("--dry-run", dest="dru_run", action="store_true",
                            help="Just do a test-run. No actual changes will be made")
    parser.add_option_group(common_group)

    thumb_group = OptionGroup(parser, "Thumbnail generation")
    thumb_group.add_option("-w", "--generate_thumbnails", dest="generate_thumbnails", action="store_true",
                      help="Creates thumbnails target folder for all photos in source folder")
    thumb_group.add_option("-o", "--dimensions", dest="thumbnail_dimensions", action="store",
                      help="""Dimensions for thumbnail in pixels, for example 400x400 (height X width).
                      Can also generate thumbnail with different dimensions by providing a list of dimensions, like:
                      -o 400x400,800x600,1024x768. NB! No spaces!""")
    thumb_group.add_option("--crop", dest="crop_thumbnails", action="store_true",
                      help="Crops thumbnails and uses width and height values as boundries")
    parser.add_option_group(thumb_group)

    add_common_options(parser)
    (options, args) = parser.parse_args()
    check_common_options(options, args)

    if not options.source and not options.target:
        print("ERROR: You must supply both source- and target-folders.\n")
        sys.exit(1)

    elif options.generate_thumbnails:
        pass


if __name__ == "__main__":
    main()