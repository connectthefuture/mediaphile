import os
import unittest
import logging
from optparse import OptionParser, OptionGroup
import shutil
import sys
from mediaphile.lib import months
from mediaphile.cli import default_timestamp_format, default_duplicate_filename_format, default_new_filename_format
from mediaphile.lib.photos import get_date_from_file, relocate_photos
from mediaphile.lib.file_operations import generate_filename_from_date



class RelocatePhotosTests(unittest.TestCase):

    def setUp(self):
        """
        """
        self.testarea = os.path.join(os.curdir, 'testarea')
        if os.path.exists(self.testarea):
            shutil.rmtree(self.testarea)
        os.makedirs(self.testarea)
        self.testfile = os.path.join(self.testarea, 'DSC_1807.JPG')
        shutil.copy(os.path.join(os.curdir, 'Nikon', 'DSC_1807.JPG'), self.testfile)
        self.assertTrue(os.path.exists(self.testfile))

    def tearDown(self):
        """
        """
        if os.path.exists(self.testarea):
            shutil.rmtree(self.testarea)

    def file_exists(self, filename):
        if os.path.exists(filename):
            return True

        print("File not found: %s" % filename)
        counter = 0
        while (counter < 10):
            p,fname = os.path.split(filename)
            parts = [o for o in p.split(os.sep)[:-1] if o != '.' and o]
            print(os.path.join(os.curdir, os.sep.join(parts)))
            counter += 1

    def test_relocate_photos(self):
        """

        """
        dt = get_date_from_file(self.testfile)

        relocate_photos(
            source_dir=self.testarea,
            append_timestamp=True,
            remove_source=False,
            tag=None,
            dry_run=False,
            photo_extensions_to_include=['JPG', 'jpg'],
            timestamp_format=default_timestamp_format,
            duplicate_filename_format=default_duplicate_filename_format,
            new_filename_format=default_new_filename_format,
            path_prefix=None,
            skip_existing=False,
            auto_tag=False)

        self.assertTrue(self.file_exists(os.path.join(self.testarea, str(dt.year), months[dt.month], str(dt.day),
                                     generate_filename_from_date(self.testfile, dt,
                                                                 timestamp_format=default_timestamp_format,
                                                                 new_filename_format=default_new_filename_format))))

    def test_relocate_photos_with_path_prefix(self):
        """

        """
        dt = get_date_from_file(self.testfile)

        relocate_photos(
            source_dir=self.testarea,
            append_timestamp=True,
            remove_source=False,
            tag=None,
            dry_run=False,
            photo_extensions_to_include=['JPG', 'jpg'],
            timestamp_format=default_timestamp_format,
            duplicate_filename_format=default_duplicate_filename_format,
            new_filename_format=default_new_filename_format,
            path_prefix='Summer',
            skip_existing=False,
            auto_tag=False)

        self.assertTrue(self.file_exists(os.path.join(self.testarea, 'Summer', str(dt.year), months[dt.month], str(dt.day),
                                     generate_filename_from_date(self.testfile, dt,
                                                                 timestamp_format=default_timestamp_format,
                                                                 new_filename_format=default_new_filename_format))))

    def test_relocate_photos_with_path_prefix_and_tag(self):
        """

        """
        dt = get_date_from_file(self.testfile)

        relocate_photos(
            source_dir=self.testarea,
            append_timestamp=True,
            remove_source=False,
            tag='SpecialTag',
            dry_run=False,
            photo_extensions_to_include=['JPG', 'jpg'],
            timestamp_format=default_timestamp_format,
            duplicate_filename_format=default_duplicate_filename_format,
            new_filename_format=default_new_filename_format,
            path_prefix='Summer',
            skip_existing=False,
            auto_tag=False)

        self.assertTrue(self.file_exists(os.path.join(self.testarea, 'Summer', str(dt.year), months[dt.month], 'SpecialTag',
                                     generate_filename_from_date(self.testfile, dt,
                                                                 timestamp_format=default_timestamp_format,
                                                                 new_filename_format=default_new_filename_format))))

    def test_relocate_photos_with_tag(self):
        """

        """
        dt = get_date_from_file(self.testfile)

        relocate_photos(
            source_dir=self.testarea,
            append_timestamp=True,
            remove_source=False,
            tag='SpecialTag',
            dry_run=False,
            photo_extensions_to_include=['JPG', 'jpg'],
            timestamp_format=default_timestamp_format,
            duplicate_filename_format=default_duplicate_filename_format,
            new_filename_format=default_new_filename_format,
            path_prefix=None,
            skip_existing=False,
            auto_tag=False)

        self.assertTrue(self.file_exists(os.path.join(self.testarea, str(dt.year), months[dt.month], 'SpecialTag',
                                     generate_filename_from_date(self.testfile, dt,
                                                                 timestamp_format=default_timestamp_format,
                                                                 new_filename_format=default_new_filename_format))))

    def test_relocate_photos_with_auto_tag(self):
        """

        """
        new_tag = 'Tagged'
        new_folder = os.path.join(self.testarea, new_tag)
        os.makedirs(new_folder)
        new_target_file = os.path.join(new_folder, os.path.split(self.testfile)[1])
        shutil.move(self.testfile, new_target_file)
        dt = get_date_from_file(new_target_file)

        relocate_photos(
            source_dir=new_folder,
            append_timestamp=True,
            remove_source=False,
            tag=None,
            dry_run=False,
            photo_extensions_to_include=['JPG', 'jpg'],
            timestamp_format=default_timestamp_format,
            duplicate_filename_format=default_duplicate_filename_format,
            new_filename_format=default_new_filename_format,
            path_prefix=None,
            skip_existing=False,
            auto_tag=True)

        self.assertTrue(self.file_exists(os.path.join(self.testarea, str(dt.year), months[dt.month], new_tag,
                                     generate_filename_from_date(new_target_file, dt,
                                                                 timestamp_format=default_timestamp_format,
                                                                 new_filename_format=default_new_filename_format))))

    def test_relocate_photos_with_no_auto_tag(self):
        """

        """
        new_tag = 'Tagged'
        new_folder = os.path.join(self.testarea, new_tag)
        os.makedirs(new_folder)
        new_target_file = os.path.join(new_folder, os.path.split(self.testfile)[1])
        shutil.move(self.testfile, new_target_file)
        dt = get_date_from_file(new_target_file)

        relocate_photos(
            source_dir=new_folder,
            append_timestamp=True,
            remove_source=False,
            tag=None,
            dry_run=False,
            photo_extensions_to_include=['JPG', 'jpg'],
            timestamp_format=default_timestamp_format,
            duplicate_filename_format=default_duplicate_filename_format,
            new_filename_format=default_new_filename_format,
            path_prefix=None,
            skip_existing=False,
            auto_tag=False)

        self.assertTrue(self.file_exists(os.path.join(self.testarea, str(dt.year), months[dt.month], str(dt.day),
                                     generate_filename_from_date(new_target_file, dt,
                                                                 timestamp_format=default_timestamp_format,
                                                                 new_filename_format=default_new_filename_format))))

    def test_relocate_photos_with_auto_tag_and_custom_tag(self):
        """

        """
        new_tag = 'Tagged'
        new_folder = os.path.join(self.testarea, new_tag)
        os.makedirs(new_folder)
        new_target_file = os.path.join(new_folder, os.path.split(self.testfile)[1])
        shutil.move(self.testfile, new_target_file)
        dt = get_date_from_file(new_target_file)

        relocate_photos(
            source_dir=new_folder,
            append_timestamp=True,
            remove_source=False,
            tag="CustomTag",
            dry_run=False,
            photo_extensions_to_include=['JPG', 'jpg'],
            timestamp_format=default_timestamp_format,
            duplicate_filename_format=default_duplicate_filename_format,
            new_filename_format=default_new_filename_format,
            path_prefix=None,
            skip_existing=False,
            auto_tag=True)

        self.assertTrue(self.file_exists(os.path.join(self.testarea, str(dt.year), months[dt.month], new_tag, "CustomTag",
                                     generate_filename_from_date(new_target_file, dt,
                                                                 timestamp_format=default_timestamp_format,
                                                                 new_filename_format=default_new_filename_format))))


def main():
    parser = OptionParser()
    common_group = OptionGroup(parser, "Test parameters")
    common_group.add_option("-v", "--verbose", dest="verbose", help="enable verbose logging of test data",
                            action="store_true")
    parser.add_option_group(common_group)

    (options, args) = parser.parse_args()
    if options.verbose:
        logging.basicConfig(stream=sys.stdout)
        logging.getLogger("verbose").setLevel(logging.DEBUG)

    unittest.main()

if __name__ == '__main__':
    #PerformanceLogger.enable()
    main()
