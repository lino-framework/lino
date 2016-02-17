from __future__ import print_function
from builtins import object
class Parametrizable(object):
    parameters = None


class Table(Parametrizable):

    @classmethod
    def show(cls):
        print("This is {0} with parameters = {1}".format(cls, cls.parameters))


class Journals(Table):
    parameters = dict(foo=1, bar=2)


class AnotherTable(Table):
    pass


class MyJournals(Journals, AnotherTable):
    pass


MyJournals.show()
