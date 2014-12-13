# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines some system models, especially the :class:`SiteConfig` model.

This app should usually be installed in every Lino application.
But there are exceptions, e.g. :ref:`lino.tutorial.polls`
or :doc:`/tutorials/de_BE/index` don't.

.. autosummary::
   :toctree:

   models
   mixins
   tests


"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("System")

