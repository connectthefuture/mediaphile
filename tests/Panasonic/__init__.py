import os
import unittest
from mediaphile.test import PhotosWithMetadata


class PanasonicTests(PhotosWithMetadata):
    """
    Tests the most basic functions and methods in photofile in relation to photos produced using Panasonic cameras,
    like Lumix DMC-FS9 and ???.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'Panasonic')
        self.photo_extensions_to_include = ['jpg']


if __name__ == '__main__':
    unittest.main()
