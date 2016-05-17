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

from .choicelists import BuildMethod, BuildMethods
from .actions import BasePrintAction


class PrintableObject(object):
    
    def get_template_groups(self):
        return [self.__class__.get_template_group()]

    def get_print_templates(self, bm, action):
        """Return a list of filenames of templates for the specified
        build method.  Returning an empty list means that this item is
        not printable.  For subclasses of :class:`SimpleBuildMethod`
        the returned list may not contain more than 1 element.

        The default method calls
        :meth:`BuildMethod.get_default_template` and returns this as a
        list with one item.

        """
        return [bm.get_default_template(self)]

    def get_default_build_method(self):
        return BuildMethods.get_system_default()

    def get_build_method(self):
        """Return the build method to use when printing this object.

        This is expected to rather raise an exception than return
        `None`.

        """
        # TypedPrintable  overrides this
        return self.get_default_build_method()

    def get_build_options(self, bm, **opts):
        # header_center
        return opts


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



