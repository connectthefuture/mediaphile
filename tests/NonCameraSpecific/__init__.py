import os
import unittest
from mediaphile.test import PhotosWithoutMetadata


class NonCameraSpecificTests(PhotosWithoutMetadata):
    """
    Tests the most basic functions and methods in photofile, in relation to photos or images not produced by cameras,
    missing EXIF- and IPTC-information.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'NonCameraSpecific')
        self.photo_extensions_to_include = ['bmp', 'gif', 'jpg', 'tiff', 'tif', 'png']


if __name__ == '__main__':
    unittest.main()
