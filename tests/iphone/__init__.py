import os
import unittest
from mediaphile.test import PhotosWithMetadata, PhotosWithGPSMetadata


class iPhone4Tests(PhotosWithMetadata, PhotosWithGPSMetadata):
    """
    Tests the most basic functions and methods in photofile in relation photos taken with iPhone 4.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'iphone', 'iPhone4')
        self.photo_extensions_to_include = ['jpg']
        self.expected_make = 'Apple'
        self.expected_model = 'iPhone 4'


if __name__ == '__main__':
    unittest.main()
