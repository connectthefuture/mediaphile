import os
import unittest
from photofile.xmp import get_xmp_value


class XmpTests(unittest.TestCase):
    """
    Tests the most basic functions and methods in photofile in relation to metadata stored in sidecar files like files
    produced from Corel AfterShot Pro.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.path.abspath(os.curdir), 'XMP')

    def test_caption(self):
        """

        """
        input_file = os.path.join(self.source_folder, 'DSC_1807_20060417_134347.JPG.xmp')
        print(get_xmp_value(input_file, 'caption'))



if __name__ == '__main__':
    unittest.main()