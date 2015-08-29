from lino.utils.pythontest import TestCase


class DocTest(TestCase):

    def test_files(self):

        self.check_doctest('index.rst')
        from django import VERSION
        if VERSION[0] == 1 and VERSION[1] == 6:
            self.check_doctest('django16.rst')
        elif VERSION[0] == 1 and VERSION[1] > 6:
            self.check_doctest('django17.rst')
        else:
            self.fail("Unsupported Django version {0}".format(VERSION))

