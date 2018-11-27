# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from .choicelists import BuildMethod, BuildMethods
from .actions import BasePrintAction


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



