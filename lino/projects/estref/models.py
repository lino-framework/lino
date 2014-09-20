# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module for :ref:`estref` app.

"""

from lino import dd, rt


def site_setup(site):
    site.modules.countries.Places.required = dd.required(auth=False)
    site.modules.countries.Countries.required = dd.required(auth=False)

