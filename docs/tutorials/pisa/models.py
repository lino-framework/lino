from lino import mixins


class Person(mixins.Human, mixins.Printable):
    pass


