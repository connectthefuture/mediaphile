import os
import unittest


class iPhoneTests(unittest.TestCase):
    """
    Tests the most basic functions and methods in photofile in relation photos taken with iPhone, iPad, iPod etc.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'iphone')


if __name__ == '__main__':
    unittest.main()