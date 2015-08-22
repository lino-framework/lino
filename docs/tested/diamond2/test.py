from lino.utils.pythontest import TestCase


class DocTest(TestCase):

    def test_files(self):

        self.check_doctest('index.rst')
        from django import VERSION
        self.assertEqual(VERSION[0], 1)
        if VERSION[1] == 6:
            self.check_doctest('django16.rst')
        elif VERSION[1] > 6:
            self.check_doctest('django17.rst')
        else:
            self.fail("Unsupported Django version {0}".format(VERSION))

