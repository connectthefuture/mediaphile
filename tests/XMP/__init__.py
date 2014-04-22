import os
import unittest
from photofile.utils import get_photos_in_folder, get_date_from_file, generate_filename_from_date, \
    generate_folders_from_date
from photofile.metadata import get_metadata, get_exif


class XmpTests(unittest.TestCase):
    """
    Tests the most basic functions and methods in photofile in relation to metadata stored in sidecar files like files
    produced from Corel AfterShot Pro.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'XMP')

    def test_caption(self):
        """

        """


if __name__ == '__main__':
    unittest.main()