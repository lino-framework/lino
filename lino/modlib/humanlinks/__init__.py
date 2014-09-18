# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines "parency links" or "human links", i.e. links between two humans.

Main user interface is "parents" and "children" of a "human".

**Settings**

.. setting:: humanlinks.human_model

A string referring to the model which represents a human in your
application.
Default value is ``'contacts.Person'``.

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "Ceci n'est pas une documentation."
    verbose_name = _("Parency links")

    ## settings
    human_model = 'contacts.Person'

