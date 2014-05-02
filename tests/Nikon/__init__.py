import os
import unittest
from mediaphile.test import PhotosWithMetadata


class NikonTests(PhotosWithMetadata):
    """
    Tests the most basic functions and methods in photofile, in relation to photos produced using Nikon cameras like
    D70 and D90.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'Nikon')
        self.photo_extensions_to_include = ['jpg', 'nef']
        #self.expected_make = 'NIKON CORPORATION'


if __name__ == '__main__':
    unittest.main()