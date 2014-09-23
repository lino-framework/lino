# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"See :mod:`ml.contacts`."

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
