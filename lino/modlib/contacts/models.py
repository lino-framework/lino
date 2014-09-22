# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)


"""The :xfile:`models.py` module for the :mod:`lino.modlib.contacs`
app.


See :mod:`ml.contacts`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from lino import dd, rt

from lino import mixins

from lino.utils import join_words
from lino.utils import join_elems
from lino.utils.choosers import chooser

from lino.modlib.countries.models import AddressLocation

from lino.modlib.contacts import Plugin

from lino.utils import mti
from lino.utils.xmlgen.html import E


PARTNER_NUMBERS_START_AT = 100  # used for generating demo data and tests


class CompanyType(dd.BabelNamed):

    class Meta:
        verbose_name = _("Organization type")
        verbose_name_plural = _("Organization types")

    abbr = dd.BabelCharField(_("Abbreviation"), max_length=30, blank=True)


class CompanyTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = 'contacts.CompanyType'
    column_names = 'name *'
    #~ label = _("Company types")


class Partner(dd.Polymorphic, AddressLocation, dd.Addressable):
    "See :class:`ml.contacts.Partner`."

    preferred_foreignkey_width = 20
    # preferred width for ForeignKey fields to a Partner

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Partner')
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    name = models.CharField(max_length=200, verbose_name=_('Name'))

    language = dd.LanguageField()

    email = models.EmailField(_('E-Mail'), blank=True)  # ,null=True)
    url = models.URLField(_('URL'), blank=True)
    phone = models.CharField(_('Phone'), max_length=200, blank=True)
    gsm = models.CharField(_('GSM'), max_length=200, blank=True)
    fax = models.CharField(_('Fax'), max_length=200, blank=True)

    remarks = models.TextField(_("Remarks"), blank=True)  # ,null=True)

    is_person = mti.EnableChild(
        "contacts.Person",
        verbose_name=_("is Person"),
        help_text=_("Whether this Partner is a Person."))

    is_company = mti.EnableChild(
        "contacts.Company",
        verbose_name=_("is Company"),
        help_text=_("Whether this Partner is a Company."))

    print_labels = dd.PrintLabelsAction()

    def on_create(self, ar):
        self.language = ar.get_user().language
        if not self.country:
            sc = settings.SITE.site_config
            if sc.site_company:
                self.country = sc.site_company.country
        super(Partner, self).on_create(ar)

    def save(self, *args, **kw):
        if self.id is None:
            sc = settings.SITE.site_config
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        #~ logger.info("20120327 Partner.save(%s,%s)",args,kw)
        super(Partner, self).save(*args, **kw)

    def __unicode__(self):
        #~ return self.name
        return self.get_full_name()

    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()

    def get_full_name(self, *args, **kw):
        """\
Returns a one-line string representing this Partner.
The default returns simply the `name` field, ignoring any parameters,
but e.g. :class:`Human` overrides this.
        """
        return self.name
    full_name = property(get_full_name)

    @dd.displayfield(_("Name"))
    def name_column(self, request):
        #~ return join_words(self.last_name.upper(),self.first_name)
        return unicode(self)

    def get_partner_instance(self):
        return self  # compatibility with lino.modlib.partners

    def get_name_elems(self, ar):
        return [E.b(self.name), E.br()]

    @dd.displayfield()
    def overview(self, ar):
        return E.div(*self.get_overview_elems(ar))

    def get_overview_elems(self, ar):
        elems = self.get_name_elems(ar)
        elems += join_elems(list(self.address_location_lines()), sep=E.br)
        elems = [
            E.div(*elems,
                  style="font-size:18px;font-weigth:bold;"
                  "vertical-align:bottom;text-align:middle")]
        return elems


class PartnerDetail(dd.FormLayout):

    main = """
    address_box:60 contact_box:30
    bottom_box
    """

    address_box = dd.Panel("""
    name_box
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """, label=_("Address"))

    contact_box = dd.Panel("""
    info_box
    email:40
    url
    phone
    gsm fax
    """, label=_("Contact"))

    bottom_box = """
    remarks
    is_person is_company #is_user
    """

    name_box = "name"
    info_box = "id language"


class Partners(dd.Table):
    required = dd.Required(user_level='user')  # user_groups='office')
    model = 'contacts.Partner'
    column_names = "name email * id"
    order_by = ['name', 'id']
    #~ column_names = "name * id"
    detail_layout = PartnerDetail()
    insert_layout = dd.FormLayout("""
    name
    language email
    """, window_size=(40, 'auto'))

    @classmethod
    def get_queryset(self, ar):
        return self.model.objects.select_related('country', 'city')


#~ class AllPartners(Partners):

    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return _("All %s") % self.model._meta.verbose_name_plural

class PartnersByCity(Partners):
    master_key = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 name language *"


class PartnersByCountry(Partners):
    master_key = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()


class Person(mixins.Human, mixins.Born, Partner):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Person')
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        ordering = ['last_name', 'first_name']

    title = models.CharField(
        max_length=200, blank=True,
        verbose_name=_('Title'),
        help_text=_(
            "Text to print before allocation and name as part "
            "of the first address line."))

    def full_clean(self, *args, **kw):
        """Set the `name` field of this person.  This field is visible in the
        Partner's detail but not in the Person's detail and serves for
        sorting when selecting a Partner.  It also serves for quick
        search on Persons.

        """
        self.name = join_words(self.last_name, self.first_name)
        super(Person, self).full_clean(*args, **kw)

    def address_person_lines(self, *args, **kw):
        "Deserves more documentation."
        if self.title:
            yield self.title
        yield self.get_full_name(*args, **kw)
        #~ l = filter(lambda x:x,[self.first_name,self.last_name])
        #~ yield  " ".join(l)

    def get_name_elems(self, ar):
        elems = [self.get_salutation(nominative=True), E.br()]
        if self.title:
            elems += [self.title, ' ']
        elems += [self.first_name, ' ',
                  E.b(self.last_name),
                  E.br()]
        return elems


class PersonDetail(PartnerDetail):

    name_box = "last_name first_name:15 gender title:10"
    info_box = "id:5 language:10"
    bottom_box = "remarks contacts.RolesByPerson"


class Persons(Partners):

    """
    List of all Persons.
    """
    #~ required = dict(user_level='user')
    model = "contacts.Person"
    order_by = ["last_name", "first_name", "id"]
    column_names = (
        "name_column:20 address_column email "
        "phone:10 gsm:10 id language:10 *")
    detail_layout = PersonDetail()

    insert_layout = dd.FormLayout("""
    first_name last_name
    gender language
    """, window_size=(60, 'auto'))


class Company(Partner):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Company')
        app_label = 'contacts'
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    prefix = models.CharField(max_length=200, blank=True)

    type = models.ForeignKey('contacts.CompanyType', blank=True, null=True)

    def get_full_name(self, salutation=True, **salutation_options):
        """Deserves more documentation."""
        #~ print '20120729 Company.get_full_name`'
        if self.type:
            return join_words(self.prefix, self.type.abbr, self.name)
        return join_words(self.prefix, self.name)
    full_name = property(get_full_name)

    def get_name_elems(self, ar):
        elems = []
        if self.prefix:
            elems += [self.prefix, ' ']
        elems += [E.b(self.name), E.br()]
        return elems


class CompanyDetail(PartnerDetail):

    bottom_box = """
    remarks contacts.RolesByCompany
    """

    name_box = "prefix:10 name type:30"


class Companies(Partners):
    model = "contacts.Company"
    order_by = ["name"]
    detail_layout = CompanyDetail()
    insert_layout = dd.FormLayout("""
    name
    language:20 email:40
    type id
    """, window_size=(60, 'auto'))

#~ class List(Partner):
    #~ pass

#~ class Lists(Partners):
    #~ model = List
    #~ order_by = ["name"]
    #~ detail_layout = """
    #~ id name
    #~ language email
    #~ MembersByList
    #~ """
    #~ insert_layout = dd.FormLayout("""
    #~ name
    #~ language email
    #~ """,window_size=(40,'auto'))


# class ContactType(dd.BabelNamed):
class RoleType(dd.BabelNamed):

    """
    TODO: rename "RoleType" to "Function" or "ContactType".
    
    RoleType,name is used at "in seiner Eigenschaft als ..." 
    in document templates for contracts.    
    """
    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")


class RoleTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = RoleType


#~ class Contact(dd.Model):
class Role(dd.Model, dd.Addressable):

    """
    
    A Contact (historical model name :class:`Role`) 
    is a :class:`Person` 
    that has a given  role (:class:`ContactType`) 
    in a given :class:`Company`. 
    
    TODO: rename "Role" to "Contact".
    """

    class Meta:
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")

    type = models.ForeignKey('contacts.RoleType',
                             blank=True, null=True,
                             verbose_name=_("Contact Role"))
    person = models.ForeignKey("contacts.Person", related_name='rolesbyperson')
    company = models.ForeignKey(
        "contacts.Company", related_name='rolesbycompany')
    #~ type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))

    #~ def __unicode__(self):
        #~ if self.person_id is None:
            #~ return super(Contact,self).__unicode__()
        #~ if self.type is None:
            #~ return unicode(self.person)
        #~ return u"%s (%s)" % (self.person, self.type)

    def __unicode__(self):
        if self.person_id is None:
            return super(Role, self).__unicode__()
        if self.type is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.type)

    #~ def address_lines(self):
        #~ for ln in self.person.address_person_lines():
            #~ yield ln
        #~ if self.company:
            #~ for ln in self.company.address_person_lines():
                #~ yield ln
            #~ for ln in self.company.address_location_lines():
                #~ yield ln
        #~ else:
            #~ for ln in self.person.address_location_lines():
                #~ yield ln
    def address_person_lines(self):
        #~ yield self.name
        if self.company:
            for ln in self.company.address_person_lines():
                yield ln
        for ln in self.person.address_person_lines():
            yield ln

    def address_location_lines(self):
        if self.company:
            return self.company.address_location_lines()
        else:
            return self.person.address_location_lines()

#~ class ContactsByCompany(dd.Table):
    #~ model = 'contacts.RoleOccurence'
    #~ master_key = 'company'
    #~ column_names = 'person type *'

#~ class ContactsByPerson(dd.Table):
    #~ label = _("Contact for")
    #~ model = 'contacts.RoleOccurence'
    #~ master_key = 'person'
    #~ column_names = 'company type *'


class Roles(dd.Table):
    required = dd.required(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = 'contacts.Role'


class RolesByCompany(Roles):
    required = dd.required()
    auto_fit_column_widths = True
    #~ required_user_level = None
    label = _("Contact persons")
    master_key = 'company'
    column_names = 'person type *'
    hidden_columns = 'id'


class RolesByPerson(Roles):
    required = dd.required()
    #~ required_user_level = None
    label = _("Contact for")
    master_key = 'person'
    column_names = 'company type *'
    auto_fit_column_widths = True
    hidden_columns = 'id'


class PartnerDocument(dd.Model):

    """
    Adds two fields 'partner' and 'person' to this model, 
    making it something that refers to a "partner". 
    `person` means a "contact person" for the partner.
    
    """

    class Meta:
        abstract = True

    company = models.ForeignKey("contacts.Company",
                                blank=True, null=True)

    person = models.ForeignKey("contacts.Person", blank=True, null=True)

    def get_partner(self):
        if self.company is not None:
            return self.company
        return self.person

    def get_mailable_recipients(self):
        for p in self.company, self.person:
            if p is not None and p.email:
                #~ yield "%s <%s>" % (p, p.email)
                yield ('to', p)
                #~ yield ('to', unicode(p), p.email)

    def get_postable_recipients(self):
        for p in self.company, self.person:
            if p is not None:
                yield p

    def summary_row(self, ar, **kw):
        """
        A :meth:`lino.core.model.Model.summary_row` 
        method for partner documents.
        """
        href_to = ar.obj2html
        s = [href_to(self)]
        #~ if self.person and not dd.has_fk(rr,'person'):
        if self.person:
            if self.company:
                s += [" (", href_to(self.person),
                      "/", href_to(self.company), ")"]
            else:
                s += [" (", href_to(self.person), ")"]
        elif self.company:
            s += [" (", href_to(self.company), ")"]
        return s

    def update_owned_instance(self, other):
        #~ print '20120627 PartnerDocument.update_owned_instance'
        if isinstance(other, mixins.ProjectRelated):
            if isinstance(self.person, Person):
                other.project = self.person
            elif isinstance(self.company, Person):
                other.project = self.company
        other.person = self.person
        other.company = self.company
        super(PartnerDocument, self).update_owned_instance(other)


class OldCompanyContact(dd.Model):

    """
    Abstract class which adds two fields `company` and `contact`.
    """
    class Meta:
        abstract = True

    company = models.ForeignKey("contacts.Company",
                                related_name="%(app_label)s_%(class)s_set_by_company",
                                verbose_name=_("Company"),
                                blank=True, null=True)

    contact = models.ForeignKey("contacts.Role",
                                related_name="%(app_label)s_%(class)s_set_by_contact",
                                blank=True, null=True,
                                verbose_name=_("represented by"))

    @chooser()
    def contact_choices(cls, company):
        if company is not None:
            return cls.contact_choices_queryset(company)
        return []

    @classmethod
    def contact_choices_queryset(cls, company):
        return Role.objects.filter(company=company)

    def full_clean(self, *args, **kw):
        if self.company:
            if self.contact is None \
                or self.contact.company is None \
                    or self.contact.company.pk != self.company.pk:
                qs = self.contact_choices_queryset(self.company)
                #~ qs = self.company.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact = None
        super(CompanyContact, self).full_clean(*args, **kw)


class ContactRelated(dd.Model):

    """Abstract class for things that relate to a company represented by
    a person as a given role.

    Adds 3 fields `company`, `contact_person` and `contact_role`.

    """

    class Meta:
        abstract = True

    company = models.ForeignKey(
        "contacts.Company",
        related_name="%(app_label)s_%(class)s_set_by_company",
        verbose_name=_("Company"),
        blank=True, null=True)

    contact_person = models.ForeignKey(
        "contacts.Person",
        related_name="%(app_label)s_%(class)s_set_by_contact_person",
        blank=True, null=True,
        verbose_name=_("represented by"))

    contact_role = models.ForeignKey(
        "contacts.RoleType",
        related_name="%(app_label)s_%(class)s_set_by_contact_role",
        blank=True, null=True,
        verbose_name=_("represented as"))

    @chooser()
    def contact_person_choices(cls, company):
        """
        chooser method for the `contact_person` field.
        """
        if company is not None:
            return cls.contact_person_choices_queryset(company)
        return rt.modules.contacts.Person.objects.order_by(
            'last_name', 'first_name')

    def get_contact(self):
        if self.contact_person is not None:
            if self.company is not None:
                roles = Role.objects.filter(
                    company=self.company, person=self.contact_person)
                #~ print '20120929 get_contact', roles
                if roles.count() == 1:
                    return roles[0]

    def get_recipient(self):
        contact = self.get_contact()
        if contact is not None:
            return contact
        if self.contact_person is not None:
            if self.company is not None:
                return Role(company=self.company, person=self.contact_person)
            return self.contact_person
        return self.company

    recipient = property(get_recipient)

    def get_partner(self):
        return self.company or self.contact_person
    partner = property(get_partner)
    """(read-only property) \
    The "legal partner", \
    i.e. usually the :class:`Company` instance pointed to by \
    the `company` field, \
    except when that field is empty, in which case `partner` \
    contains the :class:`Person` pointed to by the \
    `contact_person` field.
    If both fields are empty, then `partner` contains `None`.
    """

    def contact_person_changed(self, ar):
        #~ print '20120929 contact_person_changed'
        if self.company and not self.contact_person_id:
            roles = Role.objects.filter(company=self.company)
            if roles.count() == 1:
                self.contact_person = roles[0].person
                self.contact_role = roles[0].type
            return

    @classmethod
    def contact_person_choices_queryset(cls, company):
        """
        Return a queryset of candidate Person objects allowed
        in `contact_person` for a given `company`.
        """
        return settings.SITE.modules.contacts.Person.objects.filter(
            rolesbyperson__company=company).distinct()

    def full_clean(self, *args, **kw):
        if not settings.SITE.loading_from_dump:
            if self.company is not None and self.contact_person is None:
                qs = self.contact_person_choices_queryset(self.company)
                #~ qs = self.company.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact_person = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact_person = None
            contact = self.get_contact()
            if contact is not None:
                self.contact_role = contact.type
                #~ print '20120929b', contact.type
        super(ContactRelated, self).full_clean(*args, **kw)


dd.inject_field(
    'system.SiteConfig',
    'next_partner_id',
    models.IntegerField(
        default=PARTNER_NUMBERS_START_AT,
        blank=True, null=True,
        verbose_name=_("Next partner id"),
        help_text=_("The next automatic id for any new partner.")))

dd.inject_field(
    'system.SiteConfig',
    'site_company',
    models.ForeignKey(
        "contacts.Company",
        blank=True, null=True,
        verbose_name=_("Site owner"),
        related_name='site_company_sites',
        help_text=_("""The organisation who runs this site.
        This is used e.g. as sender in documents.
        Or, newly created partners inherit the country of the site owner.
        """)))


#~ dd.inject_field(Partner,
    #~ 'is_person',
    #~ mti.EnableChild(
        #~ settings.SITE.person_model,
        #~ verbose_name=_("is Person"),
        #~ help_text=_("Whether this Partner is a Person.")))
#~ dd.inject_field(Partner,
    #~ 'is_company',
    #~ mti.EnableChild(
        #~ "contacts.Company",
        #~ verbose_name=_("is Company"),
        #~ help_text=_("Whether this Partner is a Company.")))


def site_setup(site):

    site.modules.countries.Places.set_detail_layout("""
    name country
    type parent zip_code id
    PlacesByPlace
    contacts.PartnersByCity
    """)


@dd.receiver(dd.pre_analyze)
def company_model_alias(sender, **kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisation = sender.modules.contacts.Company


@dd.receiver(dd.post_analyze)
def company_tables_alias(sender, **kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisations = sender.modules.contacts.Companies


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("contacts", Plugin.verbose_name)
    # We use the string representations and not the classes because
    # other installed applications may want to override these tables.
    for a in ('contacts.Persons', 'contacts.Companies', 'contacts.Partners'):
        m.add_action(a)


def setup_master_menu(site, ui, profile, m):
    pass


def setup_config_menu(site, ui, profile, m):
    config_contacts = m.add_menu("contacts", Plugin.verbose_name)
    config_contacts.add_action(CompanyTypes)
    config_contacts.add_action(RoleTypes)
    #~ config_contacts.add_action(site.modules.countries.Countries)
    #~ config_contacts.add_action(site.modules.countries.Places)
    #~ config_contacts.add_action(site.modules.countries.Languages)

    #~ m  = m.add_menu("contacts",_("~Contacts"))
    #~ m.add_action('contacts.RoleTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("contacts", Plugin.verbose_name)
    m.add_action(site.modules.contacts.Roles)
    #~ m.add_action(site.modules.countries.Places)

#~ def setup_quicklinks(site,ui,user,m):
    #~ m.add_action(Person.detail_action)


def PartnerField(**kw):
    return models.ForeignKey(Partner, **kw)
