# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :mod:`lino.modlib.contacts` package provides models and
functionality for managing contacts.

See also :mod:`ml.contacts`.

.. autosummary::
   :toctree:

    models
    utils
    mixins
    dummy
    fixtures.std
    fixtures.demo
    fixtures.demo_ee
    fixtures.demo_fr

"""

from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Contacts")

    ## settings
    hide_region = False
    region_label = _('Region')

    def before_analyze(self, site):
        contacts = site.modules.contacts

        if self.hide_region:
            for m in (contacts.Person, contacts.Company):
                m.hide_elements('region')
    
        if False:  # see tickets/90
            from lino import dd
            for m in (contacts.Person, contacts.Company):
                m.define_action(merge_row=dd.MergeAction(m))
            
            
# @dd.when_prepared('contacts.Person', 'contacts.Company')
# def hide_region(model):
#     model.hide_elements('region')
