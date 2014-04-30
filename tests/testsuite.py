import unittest
from Nikon import NikonTests
from Canon import CanonTests
from Panasonic import PanasonicTests
from NonCameraSpecific import NonCameraSpecificTests
from iphone import iPhoneTests


class DummyTests(unittest.TestCase):

    def test_sandbox(self):
        """
        A place to play around
        """
        pass

if __name__ == '__main__':
    unittest.main()