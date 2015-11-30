# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Some shortcut modules which group Lino's core functionalities into
a convenient name for different usage contexts.

Common usage is to write import statements like this::

  from lino.api import ad, _

.. autosummary::
   :toctree:

   ad
   dd
   rt
   shell
   doctest
   selenium

"""

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
