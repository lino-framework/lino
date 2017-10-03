# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)


from .choicelists import BuildMethod, BuildMethods
from .actions import BasePrintAction


class PrintableObject(object):
    
    def get_template_groups(self):
        return [self.__class__.get_template_group()]

    def get_print_templates(self, bm, action):
        return [bm.get_default_template(self)]

    def get_default_build_method(self):
        return BuildMethods.get_system_default()

    def get_build_method(self):
        # TypedPrintable  overrides this
        return self.get_default_build_method()

    def get_build_options(self, bm, **opts):
        # header_center
        return opts


class CustomBuildMethod(BuildMethod):
    def build(self, ar, action, obj):
        target = action.before_build(self, obj)
        if not target:
            return
        return self.custom_build(ar, obj, target)

    def custom_build(self, ar, obj, target):
        raise NotImplementedError

    @classmethod
    def create_action(cls, *args, **kwargs):
        if cls.label is not None:
            kwargs.setdefault('label', cls.label)
        return BasePrintAction(cls(cls.name), *args, **kwargs)



