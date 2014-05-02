import logging
from optparse import OptionParser, OptionGroup
import unittest
import sys

from Nikon import NikonTests
from Canon import CanonTests
from Panasonic import PanasonicTests
from NonCameraSpecific import NonCameraSpecificTests
from iphone import iPhone4Tests


class DummyTests(unittest.TestCase):

    def test_sandbox(self):
        """
        A place to play around
        """
        pass


def main():
    parser = OptionParser()
    common_group = OptionGroup(parser, "Test parameters")
    common_group.add_option("-v", "--verbose", dest="verbose", help="enable verbose logging of test data",
                            action="store_true")
    parser.add_option_group(common_group)

    (options, args) = parser.parse_args()
    if options.verbose:
        logging.basicConfig(stream=sys.stdout)
        logging.getLogger("testlogger").setLevel(logging.DEBUG)

    unittest.main()

if __name__ == '__main__':
    main()