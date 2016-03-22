from lino.mixins import Human
from lino.modlib.printing.mixins import Printable


class Person(Human, Printable):
    pass


