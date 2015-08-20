# Copyright 2014-2015 Luc Saffre
# License: BSD, see LICENSE for more details.

"""
Overrides :mod:`lino.modlib.contacts` for :mod:`lino.projects.min2`.

.. autosummary::
   :toctree:

   models

"""

from lino.modlib.contacts import Plugin


class Plugin(Plugin):

    extends_models = ['Partner', 'Person', 'Company']
