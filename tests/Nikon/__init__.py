import os
import pprint
import unittest

from mediaphile.lib.photos import get_photos_in_folder, get_date_from_file
from mediaphile.lib.metadata import get_metadata, get_exif


class NikonTests(unittest.TestCase):
    """
    Tests the most basic functions and methods in photofile, in relation to photos produced using Nikon cameras like
    D70 and D90.
    """

    def setUp(self):
        """
        Creates some default data to base our tests on.
        """
        self.source_folder = os.path.join(os.curdir, 'Nikon')

    def _test_get_photos(self):
        """

        """
        for folder, filenames in get_photos_in_folder(self.source_folder).items():
            for filename in filenames:
                print(filename)
                complete_filename = os.path.join(folder, filename)
                import pprint
                pprint.pprint(get_metadata(complete_filename))
                pprint.pprint(get_exif(complete_filename))
                dt = get_date_from_file(complete_filename)
                #print(dt)
                #print(generate_filename_from_date(complete_filename, dt))
                #print(generate_folders_from_date(dt))

        #self.assertEqual(self.seq, range(10))
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))
        ## self.assertTrue(element in self.seq)

    def test_nef_DSC_1807_20060417_134347_handling(self):
        nef_file = os.path.join(self.source_folder, 'DSC_1807_20060417_134347.NEF')
        pprint.pprint(get_metadata(nef_file))
        pprint.pprint(get_exif(nef_file))

if __name__ == '__main__':
    unittest.main()