# Copyright 2008-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"See :mod:`ml.contacts`."

from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Contacts")

    ## settings
    hide_region = False

    def before_analyze(self, site):
        # print "20140117 on_ui_init", self.hide_region
        contacts = site.modules.contacts
        # contacts = self.app_module

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
