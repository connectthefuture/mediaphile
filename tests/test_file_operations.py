import os
import tempfile
import unittest
import time
import shutil
import logging
log = logging.getLogger("testlogger")

from mediaphile.lib.file_operations import find_duplicates, find_new_files


class FileOperationTests(unittest.TestCase):
    """
    Tests file operations.
    """
    testing_area = None

    def setUp(self):
        """

        """
        while True:
            self.testing_area = os.path.join(tempfile.gettempdir(), str(int(time.time())))
            if not os.path.exists(self.testing_area):
                break

        os.makedirs(self.testing_area)

    def create_file(self, folder, text, amount):
        """

        """
        target_folder = os.path.join(tempfile.gettempdir(), self.testing_area, folder)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        target_file_counter = 0
        while True:
            if os.path.exists(os.path.join(target_folder, '%s.txt' % target_file_counter)):
                target_file_counter += 1
            else:
                break

        target_filename = os.path.join(target_folder, '%s.txt' % target_file_counter)
        f = open(target_filename, 'w')
        f.write(text*amount)
        f.close()
        return target_filename

    def tearDown(self):
        """

        """
        shutil.rmtree(self.testing_area)

    def test_file_operations(self):
        """

        """
        # create a file in folder A
        file_a = self.create_file('A', 'foobar', 1)
        source_folder = os.path.split(file_a)[0]
        # create a file in folder B
        file_b = self.create_file('B', 'foobar', 1)
        target_folder = os.path.split(file_b)[0]
        # the files are equal so find_duplicates should return 1
        self.assertEqual(len(list(find_duplicates(source_folder, target_folder))), 1)

        # create a new file in folder A with different content
        file_c = self.create_file('A', 'foobar', 2)
        # find_duplicates should still return 1 because folder B hasn't changed
        self.assertEqual(len(list(find_duplicates(source_folder, target_folder))), 1)
        # create an equal file in folder B
        file_c = self.create_file('B', 'foobar', 2)
        # find_duplicates returns 2
        self.assertEqual(len(list(find_duplicates(source_folder, target_folder))), 2)

        # remove the last file and find_duplicates returns 1.
        os.unlink(file_c)
        self.assertEqual(len(list(find_duplicates(source_folder, target_folder))), 1)
        # change the first file we created in folder B
        open(file_b, 'w').write('test')
        # find_duplicates returns now 0
        self.assertEqual(len(list(find_duplicates(source_folder, target_folder))), 0)
        # but find_new_files returns 1 because file_b has new content
        self.assertEqual(len(list(find_new_files(source_folder, target_folder))), 1)

        # creates yet another file in folder B with similar content to the first file in that folder
        file_d = self.create_file('B', 'foobar', 1)
        # find_new_files still returns 1
        self.assertEqual(len(list(find_new_files(source_folder, target_folder))), 1)
        # creates a new file with new content in folder B
        file_d = self.create_file('B', 'foobar', 3)
        # find_new_files
        self.assertEqual(len(list(find_new_files(source_folder, target_folder))), 2)


