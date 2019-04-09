# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Adds Lino-specific Sphinx setup.

.. rst:directive:: tcname

    Used for documenting template context names. 

.. rst:role:: tcname

    Refer to a template context name defined by :rst:dir:`tcname`.


"""
from __future__ import print_function, unicode_literals
import six
# from builtins import str
# Exception occurred:
#   File "site-packages/sphinx/registry.py", line 137, in add_object_type
#     'doc_field_types': doc_field_types})
# TypeError: type() argument 1 must be string, not newstr

def my_escape(s):
    s = s.replace("\u25b6 ", "")
    return s


def menuselection_text(mi):
    s = my_escape(six.text_type(mi.label).strip())
    p = mi.parent
    while p is not None:
        if p.label:
            s = my_escape(six.text_type(p.label).strip()) + " --> " + s
        p = p.parent
    return s




def setup(app):

    app.add_object_type(str('tcname'), str('tcname'),
                        objname='template context name',
                        indextemplate='pair: %s; template context name')
    app.add_object_type(str('fixture'), str('fixture'),
                        objname='demo fixture name',
                        indextemplate='pair: %s; demo fixture name')
