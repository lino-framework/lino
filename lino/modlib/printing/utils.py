# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Utilities for `lino.modlib.printing`.

Simple example::

    from lino.modlib.printing.utils import CustomBuildMethod

    class HelloWorld(CustomBuildMethod):
        target_ext = '.txt'
        name = 'hello'
        label = _("Hello")

        def custom_build(self, ar, obj, target):
            # this is your job
            file(target).write("Hello, world!")

    class MyModel(Model):
        say_hello = HelloWorld.create_action()



"""

from .choicelists import BuildMethod
from .mixins import BasePrintAction


class CustomBuildMethod(BuildMethod):
    """For example CourseToXls.

    """
    def build(self, ar, action, obj):
        target = action.before_build(self, obj)
        if not target:
            return
        return self.custom_build(ar, obj, target)

    def custom_build(self, ar, obj, target):
        """Concrete subclasses must implement this.

        This is supposed to create a file named `target`.
        
        """
        raise NotImplementedError

    @classmethod
    def create_action(cls, *args, **kwargs):
        if cls.label is not None:
            kwargs.setdefault('label', cls.label)
        return BasePrintAction(cls(cls.name), *args, **kwargs)



