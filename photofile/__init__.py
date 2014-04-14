#!/usr/bin/env python

import os
import sys
from optparse import OptionParser
#from .utils import relocate_movies, find_new_files, relocate_photos, find_duplicates, print_tag


def print_help(parser):
    """
    Prints help for the command-line interface for photofile along with some examples of use.
    :param parser:
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
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="verbose logging")
    parser.add_option("-s", "--source", dest="source", help="the source folder to process")
    parser.add_option("-t", "--target", dest="target", help="the target folder for new files")
    parser.add_option("-m", "--relocate_movies", help="relocates movies by creation date into a date-based hierarchy",
                      dest="relocate_movies", action="store_true")
    parser.add_option("-p", "--relocate_photos",
                      help="relocates photos and images by EXIF/creation date into a date-based hierarchy",
                      dest="relocate_photos", action="store_true")
    parser.add_option("-d", "--find_duplicates", help="locates duplicates in source folder compared to target folder",
                      dest="find_duplicates")
    parser.add_option("-n", "--new_files", help="locates new files in source folder compared to target folder",
                      dest="new_files")
    parser.add_option("-x", "--delete_duplicates", action="store_true", dest="delete",
                      help="deletes any duplicate file from source folder found in both source and target folder")

    (options, args) = parser.parse_args()

    if not options.source and not options.target:
        print("ERROR: You must supply both source- and target-folders.\n")
        print_help(parser)
        sys.exit(1)

    if options.relocate_movies:
         pass#relocate_movies(options.source, options.target)
    elif options.new_files:
        pass#list(find_new_files(options.source, options.target, options.verbose))
    elif options.relocate_photos:
        pass#relocate_photos(options.source, options.target)
    elif options.find_duplicates:
        pass#find_duplicates(options.source, options.target, delete_duplicates=options.delete, options.verbose)


if __name__ == "__main__":
    main()