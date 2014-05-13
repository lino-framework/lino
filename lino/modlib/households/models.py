# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino import dd
from lino.utils import join_words, join_elems
from lino.utils import mti
from lino.utils.xmlgen.html import E

contacts = dd.resolve_app('contacts')
humanlinks = dd.resolve_app('humanlinks')

config = dd.apps.households
mnugrp = dd.apps.contacts


class Type(dd.BabelNamed):

    """
    Type of a household.
    http://www.belgium.be/fr/famille/couple/cohabitation/
    """
    class Meta:
        verbose_name = _("Household Type")
        verbose_name_plural = _("Household Types")


class Types(dd.Table):
    required = dd.required(user_level='admin')
    model = Type
    detail_layout = """
    name
    HouseholdsByType
    """


class MemberRoles(dd.ChoiceList):
    """The list of allowed choices for the role of a household member.
    """
    verbose_name = _("Role")
    verbose_name_plural = _("Roles")

add = MemberRoles.add_item
add('01', _("Head of household"), 'head')
add('02', _("Spouse"), 'spouse')
add('03', _("Partner"), 'partner')
add('04', _("Cohabitant"), 'cohabitant')
add('05', _("Child"), 'child')
add('07', _("Adopted child"), 'adopted')
add('06', _("Relative"), 'relative')
# add('10', _("Child of head"), 'child_of_head')
# add('11', _("Child of partner"), 'child_of_partner')

parent_roles = (MemberRoles.head, MemberRoles.spouse,
                MemberRoles.partner, MemberRoles.cohabitant)

child_roles = (MemberRoles.child, MemberRoles.adopted)
               # MemberRoles.child_of_head, MemberRoles.child_of_partner)


class Household(contacts.Partner):
    """
    A Household is a Partner who represents several Persons living together.
    A Household has a list of :class:`members <Member>`.
    """
    class Meta:
        abstract = dd.is_abstract_model('households.Household')
        verbose_name = _("Household")
        verbose_name_plural = _("Households")

    prefix = models.CharField(max_length=200, blank=True)
    type = models.ForeignKey(Type, blank=True, null=True)
    # head = dd.ForeignKey('contacts.Person', verbose_name=_("Chef")),

    #~ dummy = models.CharField(max_length=1,blank=True)
    # workaround for https://code.djangoproject.com/ticket/13864

    # def full_clean(self, *args, **kw):
    #     if not self.name or self.name == '-':
    #         l = []
    #         for m in self.member_set.all():
    #             if m.role.name_giving:
    #                 l.append(m.person.last_name)
    #         if len(l):
    #             self.name = '-'.join(l)
    #         else:
    #             self.name = "-"
    #     super(Household, self).full_clean(*args, **kw)

    def add_member(self, person, role=None):
        mbr = dd.modules.households.Member(
            household=self, person=person, role=role)
        mbr.full_clean()
        mbr.save()
        return mbr

    def get_full_name(self, salutation=True, **salutation_options):
        """Overrides :meth:`ml.contacts.Partner.get_full_name`."""
        return join_words(self.prefix, self.name)
    full_name = property(get_full_name)

    def __unicode__(self):
        if self.type:
            return "%s %s" % (self.type, self.get_full_name())
        return unicode(self.get_full_name())


class HouseholdDetail(dd.FormLayout):

    main = """
    type name language:10 id
    address_box
    bottom_box
    """

    # intro_box = """
    # """

    box3 = """
    country region
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    """

    box4 = """
    phone
    gsm
    email:40
    url
    """

    address_box = "box3 box4"

    bottom_box = "remarks households.MembersByHousehold"


class Households(contacts.Partners):
    model = 'households.Household'
    required = dd.Required(user_groups='office')
    order_by = ["name"]
    detail_layout = HouseholdDetail()


class HouseholdsByType(Households):
    #~ label = _("Households")
    master_key = 'type'
    #~ column_names = 'person role *'


# class Role(dd.BabelNamed):
#     """
#     The role of a :class:`Member` in a :class:`Household`.
#     """
#     class Meta:
#         verbose_name = _("Household Role")
#         verbose_name_plural = _("Household Roles")

#     name_giving = models.BooleanField(
#         _("name-giving"),
#         default=False,
#         help_text=(
#             "Whether this role is name-giving for its household. "
#             "The name of a Household is computed by joining the "
#             "`Last Name` of all name-giving members with a dash (`-`)."
#         ))


# class Roles(dd.Table):
#     model = Role
#     required = dd.required(user_level='admin')
#     detail_layout = """
#     name name_giving
#     #male
#     #female
#     MembersByRole
#     """


class Member(dd.Model):
    """
    The role of a given :class:`Person` in a given :class:`Household`.
    """

    class Meta:
        abstract = dd.is_abstract_model('households.Member')
        verbose_name = _("Household Member")
        verbose_name_plural = _("Household Members")

    allow_cascaded_delete = 'household'

    role = MemberRoles.field(
        default=MemberRoles.child, blank=True, null=True)
    # role = models.ForeignKey(
    #     'households.Role', blank=True, null=True,
    #     help_text=_("The Role of this Person in this Household."))
    household = models.ForeignKey('households.Household')
    person = models.ForeignKey(
        "contacts.Person",
        related_name='membersbyperson')
    start_date = models.DateField(_("From"), blank=True, null=True)
    end_date = models.DateField(_("Until"), blank=True, null=True)
    #~ type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))

    def __unicode__(self):
        if self.person_id is None:
            return super(Member, self).__unicode__()
        if self.role is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.role)

    def address_lines(self):
        for ln in self.person.address_person_lines():
            yield ln
        if self.household:
            for ln in self.household.address_person_lines():
                yield ln
            for ln in self.household.address_location_lines():
                yield ln
        else:
            for ln in self.address_location_lines():
                yield ln


class Members(dd.Table):
    model = 'households.Member'
    required = dd.required(user_level='admin')
    order_by = ['start_date', 'end_date']


class MembersByHousehold(Members):
    required = dd.required()
    label = _("Household Members")
    master_key = 'household'
    column_names = 'person role start_date end_date *'


class SiblingsByPerson(Members):
    """
    If the master is member of a single household, display the members
    of that Household. Otherwise display an explanation message.
    
    """
    label = _("Household composition")
    required = dd.required()
    master = 'contacts.Person'
    column_names = 'person role start_date end_date *'
    auto_fit_column_widths = True
    slave_grid_format = 'summary'
    window_size = (100, 20)

    @classmethod
    def setup_request(self, ar):
        ar.master_household = None
        mi = ar.master_instance  # a Person
        if mi is None:
            return
        M = dd.modules.households.Member
        try:
            mbr = M.objects.get(person=mi)
            ar.master_household = mbr.household
        except M.DoesNotExist:
            ar.no_data_text = _("%s is not member of any household") % mi
        except M.MultipleObjectsReturned:
            # raise Warning("%s has multiple households" % mi)
            ar.no_data_text = _("%s is member of multiple households") % mi
        
    @classmethod
    def get_filter_kw(self, ar, **kw):
        # hh = self.get_master_household(ar.master_instance)
        hh = ar.master_household
        if hh is None:
            return None
        kw.update(household=hh)
        return super(SiblingsByPerson, self).get_filter_kw(ar, **kw)

    @classmethod
    def get_slave_summary(self, obj, ar):
        # For every child, we want to display its relationship to
        # every parent of this household.
        sar = self.request(master_instance=obj)
        if sar.master_household is None:
            return E.div(ar.no_data_text)
        # obj is the Person for which we display the household

        def format_item(m):
            elems = [unicode(m.role), ': ']
            if m.person:
                elems += [obj.format_family_member(ar, m.person)]
                hl = self.find_links(ar, m.person, obj)
                if len(hl):
                    elems += [' ('] + hl + [')']
            else:
                elems += [obj.format_family_member(ar, m)]
            return elems
            
        items = []
        for m in sar.data_iterator:
            items.append(E.li(*format_item(m)))
        elems = []
        if len(items) > 0:
            elems = []
            elems.append(E.ul(*items))
        return E.div(*elems)

    @classmethod
    def find_links(self, ar, child, parent):
        types = {}  # mapping LinkType -> list of parents
        for lnk in humanlinks.Link.objects.filter(child=child):
                # child=child, parent=p):
            tt = lnk.type.as_child(lnk.child)
            l = types.setdefault(tt, [])
            l.append(lnk.parent)
        elems = []
        for tt, parents in types.items():
            if len(elems):
                elems.append(', ')
            text = join_elems(
                [parent.format_family_member(ar, p) for p in parents],
                sep=_(" and "))
            elems += [tt, _(" of ")] + text
        return elems


class CreateHousehold(dd.Action):
    show_in_bbar = False
    custom_handler = True
    label = _("Create Household")
    parameters = dict(
        head=dd.ForeignKey(
            'contacts.Person', verbose_name=_("Head of household")),
        partner=dd.ForeignKey(
            'contacts.Person', verbose_name=_("Partner"),
            blank=True, null=True),
        type=dd.ForeignKey('households.Type'))
    params_layout = """
    head
    type
    partner
    """

    def action_param_defaults(self, ar, obj, **kw):
        # logger.info("20140426")
        kw = super(CreateHousehold, self).action_param_defaults(ar, obj, **kw)
        kw.update(head=obj)
        return kw

    def run_from_ui(self, ar, **kw):
        head = ar.action_param_values.head
        partner = ar.action_param_values.partner
        name = head.last_name
        if partner:
            name += '-' + partner.last_name
        hh = dd.modules.households.Household(
            # head=head,
            type=ar.action_param_values.type, name=name)
        hh.full_clean()
        hh.save()
        # TODO: see 20140426
        # hh.add_member(head, Role.objects.get(pk=1))
        if head is not None:
            hh.add_member(head, MemberRoles.head)
        if partner is not None:
            hh.add_member(partner, MemberRoles.partner)
        hh.after_ui_create(ar)
        hh.after_ui_save(ar)
        ar.success(
            _("Household has been created"),
            close_window=True, refresh_all=True)
        ar.goto_instance(hh)

dd.inject_action(
    'contacts.Person',
    create_household=CreateHousehold())
# dd.inject_action(
#     'contacts.Person',
#     show_households=dd.ShowSlaveTable('households.MembersByPerson'))


class MembersByPerson(Members):
    required = dd.required()
    label = _("Household memberships")
    master_key = 'person'
    column_names = 'household role start_date end_date *'
    # auto_fit_column_widths = True
    # hide_columns = 'id'
    slave_grid_format = 'summary'

    @classmethod
    def get_slave_summary(self, obj, ar):
        sar = self.request(master_instance=obj)
        elems = []
        # n = sar.get_total_count()
        # if n == 0:
        #     elems += [_("Not member of any household."), E.br()]
        # else:

        items = []
        for m in sar.data_iterator:
            items.append(E.li(
                unicode(m.role), _(" in "),
                # unicode(m.household.type), " ",
                ar.obj2html(m.household)))
        if len(items) > 0:
            elems += [_("%s is") % obj]
            elems.append(E.ul(*items))
        elems += [
            E.br(), ar.instance_action_button(obj.create_household)]
        return E.div(*elems)


# class MembersByRole(Members):
#     required = dd.required()
#     master_key = 'role'
#     column_names = 'person household start_date end_date *'


dd.inject_field(
    'contacts.Partner',
    'is_household',
    mti.EnableChild(
        'households.Household',
        verbose_name=_("is Household"),
        help_text=("Whether this Partner is a Household.")))


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu(mnugrp.app_label, mnugrp.verbose_name)
    m.add_action('households.Households')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(mnugrp.app_label, mnugrp.verbose_name)
    # m.add_action(Roles)
    m.add_action(Types)


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(mnugrp.app_label, mnugrp.verbose_name)
    m.add_action('households.Members')
    m.add_action('households.MemberRoles')
