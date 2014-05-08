#!/usr/bin/env python
import os

import sys
from optparse import OptionParser, OptionGroup
from os.path import expanduser
from mediaphile.lib import sizeof_fmt, get_term_mapping
from mediaphile.lib.metadata import get_metadata
from mediaphile.lib.photos import relocate_photos, get_photos_in_folder
from mediaphile.cli import add_common_options, check_common_options, get_user_config


def print_help(parser):
    """
    Prints help for the command-line interface for photofile along with some examples of use.

    :param parser: an optparser instance.
    """
    parser.print_help()
    print("")
    print("Examples of use:")
    print("")
    home_folder = expanduser("~")
    source = os.path.join(home_folder, 'Pictures', 'New')
    target = os.path.join(home_folder, 'Pictures', 'Sorted')
    print("To relocate photos and generate a date-based hierarchy from EXIF-date:\n")
    print("mediaphile -s %s -t %s" % (source, target))


def list_photos(folder):
    """
    Lists all photos in folder with photo specific data.
    """
    config = get_user_config()
    photo_extensions_to_include = [ext.strip() for ext in config.get('options', 'photo extensions').split(',')]
    for folder, filenames in get_photos_in_folder(folder, photo_extensions_to_include=photo_extensions_to_include).items():
        print("\n%s\n" % folder)
        for filename in filenames:
            complete_filename = os.path.join(folder, filename)
            metadata = get_metadata(complete_filename)
            size = os.stat(complete_filename).st_size
            make_n_model = ''
            if metadata:
                make = get_term_mapping.get(str(metadata.get('Image Make', '')), str(metadata.get('Image Make', '')))
                model = get_term_mapping.get(str(metadata.get('Image Model', '')), str(metadata.get('Image Model', '')))
                make_n_model = model
                if not make in make_n_model:
                    make_n_model = "%s %s" % (make, model)

            print("    %-30s %-10s %-20s" % (filename, sizeof_fmt(size), make_n_model))


def main():
    """
    Command-line interface for using photo and image related functions of photofile.
    """
    parser = OptionParser()

    common_group = OptionGroup(parser, "Relocates photos and images by EXIF/creation date into a date-based hierarchy")
    common_group.add_option("-s", "--source", dest="source", help="the source folder to process")
    common_group.add_option("-t", "--target", dest="target", help="the target folder for new files")
    common_group.add_option("-d", "--delete", dest="delete", action="store_true",
                            help="delete source files when processed")
    common_group.add_option("--dry-run", dest="dry_run", action="store_true",
                            help="Just do a test-run. No actual changes will be made")
    common_group.add_option("-p", "--path-prefix", dest="path_prefix",
                            help="a prefix to prepend all files when they are processed")
    common_group.add_option("-x", "--skip-existing", dest="skip_existing", action="store_true",
                            help="skip moving existing files when processing")
    common_group.add_option("--configuration-folder", dest="configuration_folder",
                            help="folder containing mediaphile.ini to use")
    common_group.add_option("-l", "--list", dest="list", action="store_true",
                            help="list all files in source folder with photo specific data")
    common_group.add_option("-a", "--auto-tag", dest="auto_tag", action="store_true",
                            help="use prepending folders as tags instead of day part from date")
    common_group.add_option("--tag", dest="tag", help="tag to use instead of day part from date")
    parser.add_option_group(common_group)

    add_common_options(parser)
    (options, args) = parser.parse_args()
    check_common_options(options, args)

    if options.list:
        if not options.source:
            print("You must provide a source when using the -l option.")
            sys.exit(1)

        list_photos(options.source)

    elif not options.source and not options.target:
        print("ERROR: You must supply both source- and target-folders.\n")
        print_help(parser)
        sys.exit(1)

    config = get_user_config(options.configuration_folder or None)

    relocate_photos(
        source_dir=options.source,
        target_dir=options.target,
        append_timestamp=config.getboolean('options', 'append timestamp') or False,
        remove_source=options.delete,
        tag=options.tag,
        dry_run=options.dry_run,
        photo_extensions_to_include=[ext.strip() for ext in config.get('options', 'photo extensions').split(',')],
        timestamp_format=config.get('options', 'timestamp format'),
        duplicate_filename_format=config.get('options', 'duplicate filename format'),
        new_filename_format=config.get('options', 'new filename format'),
        path_prefix=options.path_prefix,
        skip_existing=options.skip_existing or config.getboolean('options', 'skip existing'),
        auto_tag=options.auto_tag or config.getboolean('options', 'auto tag'))


if __name__ == "__main__":
    main()