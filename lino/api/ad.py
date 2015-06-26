# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""A shortcut module to those parts of Lino which are used in your
:xfile:`settings.py` files and in the :xfile:`__init__.py` files of
your plugins.  

The name ``ad`` stands for "Application Design".  Application design
happens **during** the import of your Django **settings** and
**before** your **models** get imported.

.. autosummary::

"""

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino.core.plugin import Plugin
from lino.core.site import Site, TestSite, configure_plugin
