# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""
This defines the :class:`Hotkey` class and some keystrokes.

The system is not yet heavily used.

"""
from builtins import object


class Hotkey(object):
    "Represents a combination of keystrokes."
    keycode = None
    shift = False
    ctrl = False
    alt = False
    inheritable = ('keycode', 'shift', 'ctrl', 'alt')

    def __init__(self, **kw):
        for k, v in list(kw.items()):
            setattr(self, k, v)

    def __call__(self, **kw):
        for n in self.inheritable:
            if not n in kw:
                kw[n] = getattr(self, n)
            return Hotkey(**kw)

# ExtJS src/core/EventManager-more.js
RETURN = Hotkey(keycode=13)
ESCAPE = Hotkey(keycode=27)
PAGE_UP = Hotkey(keycode=33)
PAGE_DOWN = Hotkey(keycode=34)
INSERT = Hotkey(keycode=44)
DELETE = Hotkey(keycode=46)


