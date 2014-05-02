import os
import unittest
import datetime

from mediaphile.lib import months
from mediaphile.lib.file_operations import generate_filename_from_date, generate_folders_from_date
from mediaphile.lib.metadata import get_metadata
from mediaphile.lib.photos import get_photos_in_folder

import logging
log = logging.getLogger("testlogger")


def get_filename_pattern(basename, dt, ext):
    """

    """
    return '%s_%s%02d%02d_%02d%02d%02d%s' % (basename, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, ext)


def get_folder_pattern(dt):
    """

    """
    return "%s%s%s%s%s" % (dt.year, os.sep, months[dt.month], os.sep, dt.day)


class BaseTest(unittest.TestCase):
    """

    """

    def setUp(self):
        """
        Must be implemented in subclass to specify camera specific parameters.
        """
        self.photo_extensions_to_include = None
        raise Exception("Must override this is subclass.")

    def generate_test_data(self):
        """
        Creates some default data to base our tests on.
        """
        self.files = []
        for folder, filenames in get_photos_in_folder(self.source_folder, photo_extensions_to_include=self.photo_extensions_to_include).items():
            for filename in filenames:
                self.files.append(os.path.join(folder, filename))


class PhotosWithMetadata(BaseTest):
    """
    This base class provides tests common for photos containing metadata like EXIF, IPTC and XMP.
    """

    def test_photos_has_metadata_and_date(self):
        """
        This test ensures that photos generated with a specific camera contains EXIF data.
        """
        self.generate_test_data()

        for complete_filename in self.files:
            data = get_metadata(complete_filename)
            self.assertTrue(data)
            self.assertTrue('EXIF Date' in data)

    def test_generate_filename_from_date(self):
        """
        This test ensures that we can generate an expected filename based on EXIF date.
        """
        self.generate_test_data()

        for complete_filename in self.files:
            #log.debug(complete_filename)
            data = get_metadata(complete_filename)
            dt = data.get('EXIF Date')
            basename, ext = os.path.splitext(os.path.basename(complete_filename))
            self.assertEqual(generate_filename_from_date(complete_filename, dt), get_filename_pattern(basename, dt, ext))

    def test_generate_folder_from_date(self):
        """
        This test ensures that we can generate an expected folder-structure based on EXIF date.
        """
        self.generate_test_data()

        for complete_filename in self.files:
            data = get_metadata(complete_filename)
            dt = data.get('EXIF Date')
            self.assertEqual(generate_folders_from_date(dt), get_folder_pattern(dt))

    def test_make(self):
        """
        This test ensures that photos contains EXIF data about the maker of the camera
        """
        self.generate_test_data()

        for complete_filename in self.files:
            data = get_metadata(complete_filename)
            self.assertTrue(data)
            self.assertTrue('Image Make' in data)
            if hasattr(self, 'expected_make'):
                self.assertEqual(str(data['Image Make']), self.expected_make)

    def test_model(self):
        """
        This test ensures that photos contains EXIF data about the model of the camera
        """
        self.generate_test_data()

        for complete_filename in self.files:
            data = get_metadata(complete_filename)
            self.assertTrue(data)
            self.assertTrue('Image Model' in data)
            if hasattr(self, 'expected_model'):
                self.assertEqual(str(data['Image Model']), self.expected_model)


class PhotosWithoutMetadata(BaseTest):
    """
    This base class provides tests common for photos without metadata like EXIF, IPTC and XMP.
    """

    def test_generate_filename_from_date(self):
        """
        This test ensures that we can generate an expected filename based on EXIF date.
        """
        self.generate_test_data()

        for complete_filename in self.files:
            data = get_metadata(complete_filename)
            if data:
                log.debug("Got unexpected metadata from %s" % complete_filename)

            st = os.stat(complete_filename)
            dt = datetime.datetime.fromtimestamp(st.st_ctime > st.st_mtime and st.st_ctime or st.st_mtime)
            basename, ext = os.path.splitext(os.path.basename(complete_filename))
            self.assertEqual(generate_filename_from_date(complete_filename, dt), get_filename_pattern(basename, dt, ext))

    def test_generate_folder_from_date(self):
        """
        This test ensures that we can generate an expected folder-structure based on EXIF date.
        """
        self.generate_test_data()

        for complete_filename in self.files:
            st = os.stat(complete_filename)
            dt = datetime.datetime.fromtimestamp(st.st_ctime > st.st_mtime and st.st_ctime or st.st_mtime)
            self.assertEqual(generate_folders_from_date(dt), get_folder_pattern(dt))


class PhotosWithGPSMetadata(BaseTest):
    """
    This base class provides tests for GPS information in photos.
    """

    def test_gps_info_available(self):
        """
        This test ensures that photos contains EXIF data about the maker of the camera
        """
        self.generate_test_data()

        for complete_filename in self.files:
            data = get_metadata(complete_filename)
            self.assertTrue(data)
            self.assertTrue('GPS GPSAltitude' in data)
            self.assertTrue('GPS GPSLatitude' in data)
            self.assertTrue('GPS GPSLongitude' in data)
