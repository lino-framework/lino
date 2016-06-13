# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for managing contacts.

.. autosummary::
   :toctree:

    roles
    models
    utils
    mixins
    dummy
    fixtures.std
    fixtures.demo
    fixtures.demo_ee
    fixtures.demo_fr
    management.commands.garble_persons


This plugin is being extended by :ref:`welfare` in
:mod:`lino_welfare.modlib.contacts` or by :ref:`voga` in
:mod:`lino_voga.modlib.contacts`.


Lino differentiates the following subclasses of Partner:

.. django2rst:: contacts.Partner.print_subclasses_graph()


The default database comes with the following list of
:class:`RoleType`:

.. django2rst:: rt.show(contacts.RoleTypes)
    

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Contacts")

    needs_plugins = ['lino.modlib.countries', 'lino.modlib.system']

    ## settings
    hide_region = False
    """Whether to hide the `region` field in postal addresses.  Set this
    to `True` if you live in a country like Belgium.  Belgium is
    --despite their constant language disputes-- obviously a very
    united country since they don't need a `region` field when
    entering a postal address.  In Belgium, when you write a letter,
    you just say the zip code and name of the city.  In many other
    countries there is a mandatory intermediate field.

    """

    region_label = _('Region')
    """The `verbose_name` of the `region` field."""

    def before_analyze(self):
        super(Plugin, self).before_analyze()
        contacts = self.site.modules.contacts
        if self.hide_region:
            for m in (contacts.Person, contacts.Company):
                m.hide_elements('region')
    
        if False:  # see tickets/90
            from lino.api import dd
            for m in (contacts.Person, contacts.Company):
                m.define_action(merge_row=dd.MergeAction(m))

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        # We use the string representations and not the classes because
        # other installed applications may want to override these tables.
        for a in ('contacts.Persons', 'contacts.Companies',
                  'contacts.Partners'):
            m.add_action(a)

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('contacts.CompanyTypes')
        m.add_action('contacts.RoleTypes')

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('contacts.Roles')



            
# @dd.when_prepared('contacts.Person', 'contacts.Company')
# def hide_region(model):
#     model.hide_elements('region')
