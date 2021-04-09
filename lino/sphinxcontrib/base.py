# -*- coding: UTF-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds Lino-specific Sphinx setup.

.. rst:directive:: tcname

    Used for documenting template context names.

.. rst:role:: tcname

    Refer to a template context name defined by :rst:dir:`tcname`.


"""

def my_escape(s):
    s = s.replace("\u25b6 ", "")
    return s


def menuselection_text(mi):
    s = my_escape(str(mi.label).strip())
    p = mi.parent
    while p is not None:
        if p.label:
            s = my_escape(str(p.label).strip()) + " --> " + s
        p = p.parent
    return s




def setup(app):

    app.add_object_type(str('tcname'), str('tcname'),
                        objname='template context name',
                        indextemplate='pair: %s; template context name')
    app.add_object_type(str('fixture'), str('fixture'),
                        objname='demo fixture name',
                        indextemplate='pair: %s; demo fixture name')
