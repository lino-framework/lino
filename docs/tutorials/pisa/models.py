from lino.mixins import Human # , Genders
from lino import dd

class Person(Human,dd.Printable):
    pass
    #~ do_print = dd.DirectPrintAction(build_method="pisa")

