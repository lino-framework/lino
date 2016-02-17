# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Model mixins for `lino.modlib.contacts`.
"""
from builtins import object

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.utils.xmlgen.html import E, lines2p


class ContactRelated(dd.Model):
    """Model mixin for things that relate to **either** a private person
    **or** a company, the latter potentially represented by a contact
    person having a given role in that company.  Typical usages are
    **invoices** or **contracts**.

    Adds 3 database fields and two virtual fields.

    .. attribute:: company

        Pointer to :class:`lino.modlib.contacts.models.Company`.

    .. attribute:: contact_person

        Pointer to :class:`lino.modlib.contacts.models.Person`.

    .. attribute:: contact_role

        The optional :class:`Role <lino.modlib.contacts.models.Role>`
        of the :attr:`contact_person` within :attr:`company`.

    .. attribute:: partner

        (Virtual field) The "legal partner", i.e. usually the
        :attr:`company`, except when that field is empty, in which
        case `partner` contains the :attr:`contact_person`.  If both
        fields are empty, then `partner` contains `None`.

    .. attribute:: recipient

        (Virtual field) The :class:`Addressable
        <lino.utils.addressable.Addressable>` object to use when
        printing a postal address for this.
        This is typically either the :attr:`company` or
        :attr:`contact_person` (if one of these fields is
        non-empty). It may also be a
        :class:`lino.modlib.contacts.models.Role` object.


    Difference between :attr:`partner` and `recipient`: an invoice can
    be issued and addressed to a given person in a company (i.e. a
    :class:`Role <lino.modlib.contacts.models.Role>` object), but
    accountants want to know the juristic person, which is either the
    :attr:`company` or a private :attr:`person` (if no :attr:`company`
    specified), but not a combination of both.

    """

    class Meta(object):
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

    @dd.chooser()
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
                roles = rt.modules.contacts.Role.objects.filter(
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
                return rt.modules.contacts.Role(
                    company=self.company, person=self.contact_person)
            return self.contact_person
        return self.company

    recipient = property(get_recipient)

    def get_partner(self):
        return self.company or self.contact_person
    partner = property(get_partner)

    def get_excerpt_options(self, ar, **kw):
        """Implements :meth:`lino.core.model.Model.get_excerpt_options`.

        """
        kw = super(ContactRelated, self).get_excerpt_options(ar, **kw)
        kw.update(company=self.company)
        kw.update(contact_person=self.contact_person)
        kw.update(contact_role=self.contact_role)
        return kw

    def has_address(self):
        """Return True if this object has a recipient which has an address.

        See
        :meth:`Addressable.has_address
        <lino.utils.addressable.Addressable.has_address>`.
        Used e.g. in xfile:`excerpts/Default.odt`

        """
        rec = self.recipient
        if rec is not None:
            return rec.has_address()
        return False

    def get_address_html(self, *args, **kwargs):
        """
        Return the address of the :attr:`recipient` of this object.
        See
        :meth:`Addressable.get_address_html
        <lino.utils.addressable.Addressable.get_address_html>`.
        """
        rec = self.get_recipient()
        if rec is None:
            return E.tostring(lines2p([], *args, **kwargs))
        return rec.get_address_html(*args, **kwargs)

    def contact_person_changed(self, ar):
        #~ print '20120929 contact_person_changed'
        if self.company and not self.contact_person_id:
            roles = rt.modules.contacts.Role.objects.filter(
                company=self.company)
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


class PartnerDocument(dd.Model):

    """Adds two fields 'partner' and 'person' to this model, making it
    something that refers to a "partner".  `person` means a "contact
    person" for the partner.

    """

    class Meta(object):
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
        if isinstance(other, dd.ProjectRelated):
            if isinstance(self.person, rt.modules.contacts.Person):
                other.project = self.person
            elif isinstance(self.company, rt.modules.contacts.Person):
                other.project = self.company
        other.person = self.person
        other.company = self.company
        super(PartnerDocument, self).update_owned_instance(other)


class OldCompanyContact(dd.Model):

    """
    Abstract class which adds two fields `company` and `contact`.
    """
    class Meta(object):
        abstract = True

    company = models.ForeignKey(
        "contacts.Company",
        related_name="%(app_label)s_%(class)s_set_by_company",
        verbose_name=_("Company"),
        blank=True, null=True)

    contact = models.ForeignKey(
        "contacts.Role",
        related_name="%(app_label)s_%(class)s_set_by_contact",
        blank=True, null=True,
        verbose_name=_("represented by"))

    @dd.chooser()
    def contact_choices(cls, company):
        if company is not None:
            return cls.contact_choices_queryset(company)
        return []

    @classmethod
    def contact_choices_queryset(cls, company):
        return rt.modules.contacts.Role.objects.filter(company=company)

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
        super(OldCompanyContact, self).full_clean(*args, **kw)


