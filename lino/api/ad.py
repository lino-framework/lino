# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.api.ad` module is a shortcut to those parts of Lino which
are used in your :xfile:`settings.py` files and in the
:xfile:`__init__.py` files of your apps.  The name ``ad`` stands for
"Application Design".  Application design happens **during** the
import of your Django **settings** and **before** your **models** get
imported.

.. autosummary::

"""

from django.utils.translation import ugettext_lazy as _

from lino.core.plugin import Plugin
from lino.core.site import Site, TestSite, configure_plugin


# __all__ = ['Site', 'TestSite', 'Plugin', 'configure_plugin', '_']
