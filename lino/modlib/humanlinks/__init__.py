# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines "parency links" between two "persons", and a user interface
to manage them.

This module is probably useful in combination with
:mod:`lino.modlib.households`.

.. autosummary::
   :toctree:

    choicelists
    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "Extends :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Parency links")

    ## settings
    person_model = 'contacts.Person'
    """
    A string referring to the model which represents a human in your
    application.  Default value is ``'contacts.Person'`` (referring to
    :class:`lino.modlib.contacts.Person`).
    """

    def setup_explorer_menu(config, site, profile, m):
        p = site.plugins.contacts
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('humanlinks.Links')
        m.add_action('humanlinks.LinkTypes')


