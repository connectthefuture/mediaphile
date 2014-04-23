#!/usr/bin/env python

import os
import sys
from optparse import OptionParser, OptionGroup
from photofile.utils import relocate_movies, find_new_files, relocate_photos, find_duplicates, print_tag
from photofile.xmp import get_xmp_value


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


def main():
    """
    Command-line interface for using photofile.
    """
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


    movie_group = OptionGroup(parser, "Movie organization")
    movie_group.add_option("-m", "--relocate_movies", help="relocates movies by creation date into a date-based hierarchy",
                      dest="relocate_movies", action="store_true")
    parser.add_option_group(movie_group)

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

    debug_group = OptionGroup(parser, "Debug options")
    debug_group.add_option("-c", "--validate_environment", dest="validate_environment", action="store_true",
                      help="Validates the python environment and checks for required packages")
    debug_group.add_option("-v", "--verbose", action="store_true", dest="verbose", help="verbose logging")
    parser.add_option_group(debug_group)

    (options, args) = parser.parse_args()

    if options.validate_environment:
        validate_environment()
        sys.exit(0)

    if options.source:
        options.source = os.path.abspath(options.source)

    if options.target:
        options.target = os.path.abspath(options.target)

    if options.sidecar_keywords and options.target:
        print(options.sidecar_keywords)
        sys.exit(0)

    elif not options.source and not options.target:
        print("ERROR: You must supply both source- and target-folders.\n")
        print_help(parser)
        sys.exit(1)

    elif options.relocate_movies:
        relocate_movies(options.source, options.target)
    elif options.new_files:
        list(find_new_files(options.source, options.target, options.verbose))
    elif options.relocate_photos:
        relocate_photos(options.source, options.target)
    elif options.find_duplicates:
        find_duplicates(options.source, options.target, delete_duplicates=options.delete, verbose=options.verbose)
    elif options.generate_thumbnails:
        find_duplicates(options.source, options.target, delete_duplicates=options.delete, verbose=options.verbose)
    elif options.validate_environment:
        validate_environment()


if __name__ == "__main__":
    main()