import os
import unittest
from mediaphile.test import PhotosWithMetadata


class CanonTests(PhotosWithMetadata):
    """
    Tests the most basic functions and methods in photofile, in relation to photos produced using Canon cameras.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'Canon')
        self.photo_extensions_to_include = ['jpg', 'cr2']


if __name__ == '__main__':
    unittest.main()