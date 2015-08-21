import unittest
import doctest


class DocTest(unittest.TestCase):

    def test_files(self):

        doctest.testfile('index.rst')
        from django import VERSION
        self.assertEqual(VERSION[0], 1)
        if VERSION[1] == 6:
            doctest.testfile('django16.rst')
        elif VERSION[1] > 6:
            doctest.testfile('django17.rst')
        else:
            self.fail("Unsupported Django version {0}".format(VERSION))

