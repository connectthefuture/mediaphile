import os
import pprint
import unittest

from mediaphile.lib import months
from mediaphile.lib.photos import get_photos_in_folder, get_date_from_file
from mediaphile.lib.metadata import get_metadata, get_exif
from mediaphile.lib.file_operations import generate_filename_from_date, generate_folders_from_date


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

    def test_get_photos(self):
        """

        """
        for folder, filenames in get_photos_in_folder(self.source_folder,
                                                      photo_extensions_to_include=['jpg', 'nef']).items():
            for filename in filenames:
                complete_filename = os.path.join(folder, filename)
                data = get_metadata(complete_filename)
                dt = data.get('EXIF Date')
                fname, ext = os.path.splitext(os.path.basename(complete_filename))
                self.assertEqual(
                    generate_filename_from_date(complete_filename, dt), '%s_%s%02d%02d_%02d%02d%02d%s' % (fname, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, ext))

                self.assertEqual(generate_folders_from_date(dt), "%s%s%s%s%02d" % (dt.year, os.sep, months[dt.month], os.sep, dt.day))
                #self.assertRaises(TypeError, random.shuffle, (1,2,3))
                ## self.assertTrue(element in self.seq)


if __name__ == '__main__':
    unittest.main()