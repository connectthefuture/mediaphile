#!/usr/bin/env python

import sys
from optparse import OptionParser, OptionGroup
from photofile.cli import cb, add_common_options, check_common_options


def main():
    """
    Command-line interface for using the XMP features of photofile.
    """
    parser = OptionParser()

    xmp_group = OptionGroup(parser, "XMP options")
    xmp_group.add_option("-i", "--search_sidecar", dest="sidecar_keywords", action="callback", callback=cb,
                      help="Searches any sidecar/XMP-files found in target for tags with a specific content")
    parser.add_option_group(xmp_group)

    add_common_options(parser)
    (options, args) = parser.parse_args()
    check_common_options(options, args)

    if options.sidecar_keywords and options.target:
        print(options.sidecar_keywords)
        sys.exit(0)

if __name__ == "__main__":
    main()