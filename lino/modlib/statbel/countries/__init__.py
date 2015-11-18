# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""An extended version of :mod:`lino.modlib.countries` which adds the
"INS code" fields to `Country` and `Place` for the classification
codes of the Belgian statistical institute .


.. autosummary::
   :toctree:

    fixtures

"""

from lino.modlib.countries import *


class Plugin(Plugin):
    extends_models = ['Country', 'Place']
